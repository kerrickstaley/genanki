from copy import copy
from cached_property import cached_property
import chevron
import yaml

class Model:

  FRONT_BACK = 0
  CLOZE = 1
  DEFAULT_LATEX_PRE = ('\\documentclass[12pt]{article}\n\\special{papersize=3in,5in}\n\\usepackage[utf8]{inputenc}\n'
                       + '\\usepackage{amssymb,amsmath}\n\\pagestyle{empty}\n\\setlength{\\parindent}{0in}\n'
                       + '\\begin{document}\n')
  DEFAULT_LATEX_POST = '\\end{document}'

  def __init__(self, model_id=None, name=None, fields=None, templates=None, css='', model_type=FRONT_BACK,
               latex_pre=DEFAULT_LATEX_PRE, latex_post=DEFAULT_LATEX_POST, sort_field_index=0):
    self.model_id = model_id
    self.name = name
    self.set_fields(fields)
    self.set_templates(templates)
    self.css = css
    self.model_type = model_type
    self.latex_pre = latex_pre
    self.latex_post = latex_post
    self.sort_field_index = sort_field_index

  def set_fields(self, fields):
    if isinstance(fields, list):
      self.fields = fields
    elif isinstance(fields, str):
      self.fields = yaml.full_load(fields)

  def set_templates(self, templates):
    if isinstance(templates, list):
      self.templates = templates
    elif isinstance(templates, str):
      self.templates = yaml.full_load(templates)

  @cached_property
  def _template_tokens(self):
    # Literal text does not make a card eligible for generation: the front must
    # contain a non-empty field after evaluating its conditional sections.
    templates = []
    for template in self.templates:
      tokens = []
      for token_type, key in chevron.tokenizer.tokenize(template['qfmt']):
        if token_type == 'literal':
          continue
        # Filters affect rendering, but card generation only checks the field.
        if token_type in ('variable', 'no escape'):
          key = key.rsplit(':', 1)[-1]
        tokens.append((token_type, key))
      templates.append(tokens)
    return templates

  def _has_field_content(self, template_ord, field_names, ignore_inverted=False):
    sections = [True]
    for token_type, key in self._template_tokens[template_ord]:
      if token_type == 'section':
        sections.append(sections[-1] and key in field_names)
      elif token_type == 'inverted section':
        sections.append(sections[-1] and (ignore_inverted or key not in field_names))
      elif token_type == 'end':
        sections.pop()
      elif token_type in ('variable', 'no escape') and sections[-1] and key in field_names:
        return True
    return False

  @cached_property
  def _req(self):
    """
    List of required fields for each template. Format is [tmpl_idx, "all"|"any"|"none", [field_ord, ...]].

    Partial reimplementation of req computing logic from Anki, using chevron to tokenize templates.

    The goal is to figure out which fields are "required", i.e. if they are missing then the front side of the note
    doesn't contain any meaningful content.
    """
    field_names = [field['name'] for field in self.fields]
    all_fields = set(field_names)

    req = []
    for template_ord in range(len(self.templates)):
      # The legacy required-fields format cannot express inverse conditions.
      # Like Anki, ignore those wrappers when computing this approximation;
      # actual card generation evaluates the original conditions per note.
      if not self._has_field_content(template_ord, all_fields, ignore_inverted=True):
        req.append([template_ord, 'none', []])
        continue

      required_fields = []
      for field_ord, field in enumerate(field_names):
        if not self._has_field_content(template_ord, all_fields - {field}, ignore_inverted=True):
          # when this field is missing, there is no meaningful content (no field values) in the question, so this field
          # is required
          required_fields.append(field_ord)

      if required_fields:
        req.append([template_ord, 'all', required_fields])
        continue

      # there are no required fields, so an "all" is not appropriate, switch to checking for "any"
      for field_ord, field in enumerate(field_names):
        if self._has_field_content(template_ord, {field}, ignore_inverted=True):
          # when this field is present, there is meaningful content in the question
          required_fields.append(field_ord)

      # Some combinations of conditions cannot be described by "all" or "any".
      # Anki uses "none" for those legacy summaries; the actual template still
      # determines which cards are generated.
      req.append([template_ord, 'any' if required_fields else 'none', required_fields])

    return req

  def to_json(self, timestamp: float, deck_id):
    for ord_, tmpl in enumerate(self.templates):
      tmpl['ord'] = ord_
      tmpl.setdefault('bafmt', '')
      tmpl.setdefault('bqfmt', '')
      tmpl.setdefault('bfont', '')
      tmpl.setdefault('bsize', 0)
      tmpl.setdefault('did', None)  # TODO None works just fine here, but should it be deck_id?

    for ord_, field in enumerate(self.fields):
      field['ord'] = ord_
      field.setdefault('font', 'Liberation Sans')
      field.setdefault('media', [])
      field.setdefault('rtl', False)
      field.setdefault('size', 20)
      field.setdefault('sticky', False)

    return {
      "css": self.css,
      "did": deck_id,
      "flds": self.fields,
      "id": str(self.model_id),
      "latexPost": self.latex_post,
      "latexPre": self.latex_pre,
      "latexsvg": False,
      "mod": int(timestamp),
      "name": self.name,
      "req": self._req,
      "sortf": self.sort_field_index,
      "tags": [],
      "tmpls": self.templates,
      "type": self.model_type,
      "usn": -1,
      "vers": []
    }

  def __repr__(self):
    attrs = ['model_id', 'name', 'fields', 'templates', 'css', 'model_type']
    pieces = ['{}={}'.format(attr, repr(getattr(self, attr))) for attr in attrs]
    return '{}({})'.format(self.__class__.__name__, ', '.join(pieces))
