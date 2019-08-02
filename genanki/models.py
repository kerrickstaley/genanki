
from .model import Model


simple_model = Model(
  1607392319,
  'Simple Model',
  fields=[
    {'name': 'Question'},
    {'name': 'Answer'},
  ],
  templates=[
        {
            'name': 'Card 1',
            'qfmt': '{{Question}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
        },
  ]
)


question_answer = Model(
    1082051613,
    'Question Answer Model',
    fields=[
        {'name': 'Question'},
        {'name': 'Answer'},
    ],
    templates=[
        {
            'name': 'Q+A Card',
            'qfmt': '{{Question}}',
            'afmt': '{{Answer}}',
        },
    ]
)
