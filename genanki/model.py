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
  def _req(self):
    """
    List of required fields for each template. Format is [tmpl_idx, "all"|"any", [req_field_1, req_field_2, ...]].

    Partial reimplementation of req computing logic from Anki. We use chevron instead of Anki's custom mustache
    implementation.

    The goal is to figure out which fields are "required", i.e. if they are missing then the front side of the note
    doesn't contain any meaningful content.
    """
    sentinel = 'SeNtInEl'
    field_names = [field['name'] for field in self.fields]

    req = []
    for template_ord, template in enumerate(self.templates):
      required_fields = []
      for field_ord, field in enumerate(field_names):
        field_values = {field: sentinel for field in field_names}
        field_values[field] = ''

        rendered = chevron.render(template['qfmt'], field_values)

        if sentinel not in rendered:
          # when this field is missing, there is no meaningful content (no field values) in the question, so this field
          # is required
          required_fields.append(field_ord)

      if required_fields:
        req.append([template_ord, 'all', required_fields])
        continue

      # there are no required fields, so an "all" is not appropriate, switch to checking for "any"
      for field_ord, field in enumerate(field_names):
        field_values = {field: '' for field in field_names}
        field_values[field] = sentinel

        rendered = chevron.render(template['qfmt'], field_values)

        if sentinel in rendered:
          # when this field is present, there is meaningful content in the question
          required_fields.append(field_ord)

      if not required_fields:
        raise Exception(
          'Could not compute required fields for this template; please check the formatting of "qfmt": {}'.format(
            template))

      req.append([template_ord, 'any', required_fields])

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
