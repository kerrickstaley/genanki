import json
import sqlite3
import zipfile

import pytest

import genanki


@pytest.fixture
def conditional_model():
  fronts = [
    '{{Question}}',
    '{{#Hint}}{{Question}}{{/Hint}}',
    '{{^Hint}}{{Question}}{{/Hint}}',
    '{{#Answer}}{{^Hint}}{{Question}}{{/Hint}}{{/Answer}}',
    '{{^Hint}}{{#Answer}}{{Question}}{{/Answer}}{{/Hint}}',
    '{{^Hint}}{{^Answer}}{{Question}}{{/Answer}}{{/Hint}}',
    '{{^Hint}}{{Question}}{{/Hint}}{{Answer}}',
    '{{#Hint}}{{^Hint}}{{Question}}{{/Hint}}{{/Hint}}',
    '{{^Hint}}SeNtInEl present{{/Hint}}{{Question}}',
    '{{^Hint}}{{^Hint}}{{Question}}{{/Hint}}{{/Hint}}',
  ]
  return genanki.Model(
    456789, 'Conditional cards',
    fields=[{'name': 'Question'}, {'name': 'Hint'}, {'name': 'Answer'}],
    templates=[{'name': 'Card {}'.format(i), 'qfmt': front, 'afmt': '{{Answer}}'}
               for i, front in enumerate(fronts)])


@pytest.mark.parametrize('fields, expected', [
  (['', '', ''], []),
  (['', '', 'answer'], [6]),
  (['', 'hint', ''], []),
  (['', 'hint', 'answer'], [6]),
  (['question', '', ''], [0, 2, 5, 6, 8, 9]),
  (['question', '', 'answer'], [0, 2, 3, 4, 6, 8, 9]),
  (['question', 'hint', ''], [0, 1, 8]),
  (['question', 'hint', 'answer'], [0, 1, 6, 8]),
])
def test_conditional_card_ordinals(conditional_model, fields, expected):
  note = genanki.Note(conditional_model, fields)
  assert [card.ord for card in note.cards] == expected


def test_legacy_requirements_ignore_inverse_wrappers(conditional_model):
  assert conditional_model.to_json(0, 0)['req'] == [
    [0, 'all', [0]],
    [1, 'all', [0, 1]],
    [2, 'all', [0]],
    [3, 'all', [0, 2]],
    [4, 'all', [0, 2]],
    [5, 'all', [0]],
    [6, 'any', [0, 2]],
    [7, 'all', [0, 1]],
    [8, 'all', [0]],
    [9, 'all', [0]],
  ]


def test_literal_text_does_not_require_fields():
  model = genanki.Model(
    456789, 'Literal text', fields=[{'name': 'Question'}, {'name': 'Answer'}],
    templates=[{'name': 'Card', 'qfmt': 'SeNtInEl present', 'afmt': '{{Answer}}'}])
  assert genanki.Note(model, ['question', 'answer']).cards == []
  assert model._req == [[0, 'none', []]]


def test_template_tokens_are_reusable(conditional_model):
  for _ in range(2):
    assert conditional_model._req[2] == [2, 'all', [0]]
    note = genanki.Note(conditional_model, ['question', '', ''])
    assert [card.ord for card in note.cards] == [0, 2, 5, 6, 8, 9]


@pytest.mark.parametrize('hint, expected', [
  ('', [1]),
  (' \t\r\n\f\v', [1]),
  ('<BR>', [1]),
  ('<br/>', [1]),
  ('<div />', [1]),
  (' <div> <br> </div>\n', [1]),
  ('</div><br>', [1]),
  ('\u00a0', [0]),
  ('&nbsp;', [0]),
  ('\u200b', [0]),
  ('<!-- -->', [0]),
  ('<span></span>', [0]),
  ('<br  >', [0]),
  ('<br\t>', [0]),
  ('<div class="x"></div>', [0]),
  ('<img src="x">', [0]),
  ('[sound:x.mp3]', [0]),
])
def test_conditional_field_emptiness(hint, expected):
  model = genanki.Model(
    456789, 'Empty fields',
    fields=[{'name': 'Question'}, {'name': 'Hint'}],
    templates=[
      {'name': 'With hint', 'qfmt': '{{#Hint}}{{Question}}{{/Hint}}', 'afmt': '{{Hint}}'},
      {'name': 'Without hint', 'qfmt': '{{^Hint}}{{Question}}{{/Hint}}', 'afmt': '{{Hint}}'},
    ])
  note = genanki.Note(model, ['question', hint])
  assert [card.ord for card in note.cards] == expected


@pytest.mark.parametrize('field_filter', ['text:', 'hint:', 'type:', 'tts en_US:', 'text:hint:'])
@pytest.mark.parametrize('front, expected', [('question', [0]), ('', []), ('<br>', [])])
def test_filtered_field_card_generation(field_filter, front, expected):
  model = genanki.Model(
    456789, 'Filtered fields',
    fields=[{'name': 'Question'}, {'name': 'Hint'}, {'name': 'Answer'}],
    templates=[{'name': 'Card', 'qfmt': '{{' + field_filter + 'Question}}', 'afmt': '{{Answer}}'}])
  note = genanki.Note(model, [front, 'hint', 'answer'])
  assert [card.ord for card in note.cards] == expected
  assert model._req == [[0, 'all', [0]]]


@pytest.mark.parametrize('hint, expected', [('', [0, 2]), ('hint', [0, 1])])
def test_field_names_with_periods(hint, expected):
  model = genanki.Model(
    456789, 'Literal field names',
    fields=[{'name': 'Question.Text'}, {'name': 'Hint.Text'}, {'name': 'Answer'}],
    templates=[
      {'name': 'Plain', 'qfmt': '{{Question.Text}}', 'afmt': '{{Answer}}'},
      {'name': 'With hint', 'qfmt': '{{#Hint.Text}}{{text:Question.Text}}{{/Hint.Text}}', 'afmt': '{{Answer}}'},
      {'name': 'Without hint', 'qfmt': '{{^Hint.Text}}{{Question.Text}}{{/Hint.Text}}', 'afmt': '{{Answer}}'},
    ])
  note = genanki.Note(model, ['question', hint, 'answer'])
  assert [card.ord for card in note.cards] == expected
  assert model._req == [[0, 'all', [0]], [1, 'all', [0, 1]], [2, 'all', [0]]]


def test_package_with_conditions_not_representable_by_legacy_requirements(tmp_path):
  model = genanki.Model(
    456789, 'Mixed conditions',
    fields=[{'name': name} for name in ['Question', 'Hint', 'Answer', 'Block']],
    templates=[
      {'name': 'Plain', 'qfmt': '{{Question}}', 'afmt': '{{Answer}}'},
      {'name': 'Conditional',
       'qfmt': '{{^Block}}{{#Question}}{{Hint}}{{/Question}}'
               '{{#Hint}}{{Answer}}{{/Hint}}{{#Answer}}{{Question}}{{/Answer}}{{/Block}}',
       'afmt': '{{Answer}}'},
    ])
  deck = genanki.Deck(123456, 'Mixed conditions')
  deck.add_note(genanki.Note(model, ['question one', 'hint', 'answer', '']))
  deck.add_note(genanki.Note(model, ['question two', 'hint', 'answer', 'blocked']))
  package_path = tmp_path / 'conditional.apkg'
  genanki.Package(deck).write_to_file(package_path)

  with zipfile.ZipFile(package_path) as package:
    package.extract('collection.anki2', tmp_path)
  with sqlite3.connect(tmp_path / 'collection.anki2') as collection:
    assert collection.execute('SELECT ord FROM cards ORDER BY id').fetchall() == [(0,), (1,), (0,)]
    models = json.loads(collection.execute('SELECT models FROM col').fetchone()[0])
    assert models[str(model.model_id)]['req'] == [[0, 'all', [0]], [1, 'none', []]]
