from cached_property import cached_property
from copy import copy
import pystache
import yaml

class Model:
  def __init__(self, model_id=None, name=None, fields=None, templates=None, css=''):
    self.model_id = model_id
    self.name = name
    self.set_fields(fields)
    self.set_templates(templates)
    self.css = css

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

    Partial reimplementation of req computing logic from Anki. We use pystache instead of Anki's custom mustache
    implementation.

    The goal is to figure out which fields are "required", i.e. if they are missing then the front side of the note
    doesn't contain any meaningful content.
    """
    sentinel = 'SeNtInEl'
    field_names = [field['name'] for field in self.fields]

    req = []
    for template_ord, template in enumerate(self.templates):
      field_values = {field: sentinel for field in field_names}
      required_fields = []
      for field_ord, field in enumerate(field_names):
        fvcopy = copy(field_values)
        fvcopy[field] = ''

        rendered = pystache.render(template['qfmt'], fvcopy)

        if sentinel not in rendered:
          # when this field is missing, there is no meaningful content (no field values) in the question, so this field
          # is required
          required_fields.append(field_ord)

      if required_fields:
        req.append([template_ord, 'all', required_fields])
        continue

      # there are no required fields, so an "all" is not appropriate, switch to checking for "any"
      field_values = {field: '' for field in field_names}
      for field_ord, field in enumerate(field_names):
        fvcopy = copy(field_values)
        fvcopy[field] = sentinel

        rendered = pystache.render(template['qfmt'], fvcopy)

        if sentinel in rendered:
          # when this field is present, there is meaningful content in the question
          required_fields.append(field_ord)

      if not required_fields:
        raise Exception(
          'Could not compute required fields for this template; please check the formatting of "qfmt": {}'.format(
            template))

      req.append([template_ord, 'any', required_fields])

    return req

  def to_json(self, now_ts, deck_id):
    for ord_, tmpl in enumerate(self.templates):
      tmpl['ord'] = ord_
      tmpl.setdefault('bafmt', '')
      tmpl.setdefault('bqfmt', '')
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
      "latexPost": "\\end{document}",
      "latexPre": "\\documentclass[12pt]{article}\n\\special{papersize=3in,5in}\n\\usepackage{amssymb,amsmath}\n"
                  "\\pagestyle{empty}\n\\setlength{\\parindent}{0in}\n\\begin{document}\n",
      "mod": now_ts,
      "name": self.name,
      "req": self._req,
      "sortf": 0,
      "tags": [],
      "tmpls": self.templates,
      "type": 0,
      "usn": -1,
      "vers": []
    }
