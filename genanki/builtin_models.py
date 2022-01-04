"""
Models that behave the same as Anki's built-in models ("Basic", "Basic (and reversed card)", "Cloze", etc.).

Note: Anki does not assign consistent IDs to its built-in models (see
    https://github.com/kerrickstaley/genanki/issues/55#issuecomment-717687667 and
    https://forums.ankiweb.net/t/exported-basic-cards-create-duplicate-card-types-when-imported-by-other-users/959 ).
    Because of this, we cannot simply call these models "Basic" etc. If we did, then when importing a genanki-generated
    deck, Anki would see a model called "Basic" which has a different model ID than its internal "Basic" model, and it
    would rename the imported model to something like "Basic-123abc". Instead, we name the models "Basic (genanki)"
    etc., which is less confusing.
"""

import warnings

from .model import Model


BASIC_MODEL = Model(
  1559383000,
  'Basic (genanki)',
  fields=[
    {
      'name': 'Front',
      'font': 'Arial',
    },
    {
      'name': 'Back',
      'font': 'Arial',
    },
  ],
  templates=[
    {
      'name': 'Card 1',
      'qfmt': '{{Front}}',
      'afmt': '{{FrontSide}}\n\n<hr id=answer>\n\n{{Back}}',
    },
  ],
  css='.card {\n font-family: arial;\n font-size: 20px;\n text-align: center;\n color: black;\n background-color: white;\n}\n',
)

BASIC_AND_REVERSED_CARD_MODEL = Model(
  1485830179,
  'Basic (and reversed card) (genanki)',
  fields=[
    {
      'name': 'Front',
      'font': 'Arial',
    },
    {
      'name': 'Back',
      'font': 'Arial',
    },
  ],
  templates=[
    {
      'name': 'Card 1',
      'qfmt': '{{Front}}',
      'afmt': '{{FrontSide}}\n\n<hr id=answer>\n\n{{Back}}',
    },
    {
      'name': 'Card 2',
      'qfmt': '{{Back}}',
      'afmt': '{{FrontSide}}\n\n<hr id=answer>\n\n{{Front}}',
    },
  ],
  css='.card {\n font-family: arial;\n font-size: 20px;\n text-align: center;\n color: black;\n background-color: white;\n}\n',
)

BASIC_OPTIONAL_REVERSED_CARD_MODEL = Model(
  1382232460,
  'Basic (optional reversed card) (genanki)',
  fields=[
    {
      'name': 'Front',
      'font': 'Arial',
    },
    {
      'name': 'Back',
      'font': 'Arial',
    },
    {
      'name': 'Add Reverse',
      'font': 'Arial',
    },
  ],
  templates=[
    {
      'name': 'Card 1',
      'qfmt': '{{Front}}',
      'afmt': '{{FrontSide}}\n\n<hr id=answer>\n\n{{Back}}',
    },
    {
      'name': 'Card 2',
      'qfmt': '{{#Add Reverse}}{{Back}}{{/Add Reverse}}',
      'afmt': '{{FrontSide}}\n\n<hr id=answer>\n\n{{Front}}',
    },
  ],
  css='.card {\n font-family: arial;\n font-size: 20px;\n text-align: center;\n color: black;\n background-color: white;\n}\n',
)

BASIC_TYPE_IN_THE_ANSWER_MODEL = Model(
  1305534440,
  'Basic (type in the answer) (genanki)',
  fields=[
    {
      'name': 'Front',
      'font': 'Arial',
    },
    {
      'name': 'Back',
      'font': 'Arial',
    },
  ],
  templates=[
    {
      'name': 'Card 1',
      'qfmt': '{{Front}}\n\n{{type:Back}}',
      'afmt': '{{Front}}\n\n<hr id=answer>\n\n{{type:Back}}',
    },
  ],
  css='.card {\n font-family: arial;\n font-size: 20px;\n text-align: center;\n color: black;\n background-color: white;\n}\n',
)

CLOZE_MODEL = Model(
  1550428389,
  'Cloze (genanki)',
  model_type=Model.CLOZE,
  fields=[
    {
      'name': 'Text',
      'font': 'Arial',
    },
    {
      'name': 'Back Extra',
      'font': 'Arial',
    },
  ],
  templates=[
    {
      'name': 'Cloze',
      'qfmt': '{{cloze:Text}}',
      'afmt': '{{cloze:Text}}<br>\n{{Back Extra}}',
    },
  ],
  css='.card {\n font-family: arial;\n font-size: 20px;\n text-align: center;\n color: black;\n background-color: white;\n}\n\n'
      '.cloze {\n font-weight: bold;\n color: blue;\n}\n.nightMode .cloze {\n color: lightblue;\n}',
)

def _fix_deprecated_builtin_models_and_warn(model, fields):
  if model is CLOZE_MODEL and len(fields) == 1:
    fixed_fields = fields + ['']
    warnings.warn(
      'Using CLOZE_MODEL with a single field is deprecated.'
      + ' Please pass two fields, e.g. {} .'.format(repr(fixed_fields))
      + ' See https://github.com/kerrickstaley/genanki#cloze_model-deprecationwarning .',
      DeprecationWarning)
    return fixed_fields

  return fields
