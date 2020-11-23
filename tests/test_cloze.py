"""Test creating Cloze cards"""
# https://apps.ankiweb.net/docs/manual20.html#cloze-deletion

import sys
from genanki import Model
from genanki import Note
from genanki import Deck
from genanki import Package


CSS = """.card {
 font-family: arial;
 font-size: 20px;
 text-align: center;
 color: black;
 background-color: white;
}

.cloze {
 font-weight: bold;
 color: blue;
}
.nightMode .cloze {
 color: lightblue;
}
"""

MY_CLOZE_MODEL = Model(
  998877661,
  'My Cloze Model',
  fields=[
    {'name': 'Text'},
    {'name': 'Extra'},
  ],
  templates=[{
    'name': 'My Cloze Card',
    'qfmt': '{{cloze:Text}}',
    'afmt': '{{cloze:Text}}<br>{{Extra}}',
  },],
  css=CSS,
  model_type=Model.CLOZE)

# This doesn't seem to be very useful but Anki supports it and so do we *shrug*
MULTI_FIELD_CLOZE_MODEL = Model(
  1047194615,
  'Multi Field Cloze Model',
  fields=[
    {'name': 'Text1'},
    {'name': 'Text2'},
  ],
  templates=[{
    'name': 'Cloze',
    'qfmt': '{{cloze:Text1}} and {{cloze:Text2}}',
    'afmt': '{{cloze:Text1}} and {{cloze:Text2}}',
  }],
  css=CSS,
  model_type=Model.CLOZE,
)


def test_cloze(write_to_test_apkg=False):
  """Test Cloze model"""
  notes = []
  assert MY_CLOZE_MODEL.to_json(0, 0)["type"] == 1

  # Question: NOTE ONE: [...]
  # Answer:   NOTE ONE: single deletion
  fields = ['NOTE ONE: {{c1::single deletion}}', '']
  my_cloze_note = Note(model=MY_CLOZE_MODEL, fields=fields)
  assert {card.ord for card in my_cloze_note.cards} == {0}
  notes.append(my_cloze_note)

  # Question: NOTE TWO: [...]              2nd deletion     3rd deletion
  # Answer:   NOTE TWO: **1st deletion**   2nd deletion     3rd deletion
  #
  # Question: NOTE TWO: 1st deletion       [...]            3rd deletion
  # Answer:   NOTE TWO: 1st deletion     **2nd deletion**   3rd deletion
  #
  # Question: NOTE TWO: 1st deletion       2nd deletion     [...]
  # Answer:   NOTE TWO: 1st deletion       2nd deletion   **3rd deletion**
  fields = ['NOTE TWO: {{c1::1st deletion}} {{c2::2nd deletion}} {{c3::3rd deletion}}', '']
  my_cloze_note = Note(model=MY_CLOZE_MODEL, fields=fields)
  assert sorted(card.ord for card in my_cloze_note.cards) == [0, 1, 2]
  notes.append(my_cloze_note)

  # Question: NOTE THREE: C1-CLOZE
  # Answer:   NOTE THREE: 1st deletion
  fields = ['NOTE THREE: {{c1::1st deletion::C1-CLOZE}}', '']
  my_cloze_note = Note(model=MY_CLOZE_MODEL, fields=fields)
  assert {card.ord for card in my_cloze_note.cards} == {0}
  notes.append(my_cloze_note)

  # Question: NOTE FOUR: [...] foo 2nd deletion bar [...]
  # Answer:   NOTE FOUR: 1st deletion foo 2nd deletion bar 3rd deletion
  fields = ['NOTE FOUR: {{c1::1st deletion}} foo {{c2::2nd deletion}} bar {{c1::3rd deletion}}', '']
  my_cloze_note = Note(model=MY_CLOZE_MODEL, fields=fields)
  assert sorted(card.ord for card in my_cloze_note.cards) == [0, 1]
  notes.append(my_cloze_note)

  if write_to_test_apkg:
    _wr_apkg(notes)


def _wr_apkg(notes):
  """Write cloze cards to an Anki apkg file"""
  deckname = 'mtherieau'
  deck = Deck(deck_id=0, name=deckname)
  for note in notes:
    deck.add_note(note)
  fout_anki = '{NAME}.apkg'.format(NAME=deckname)
  Package(deck).write_to_file(fout_anki)
  print('  {N} Notes WROTE: {APKG}'.format(N=len(notes), APKG=fout_anki))


def test_cloze_multi_field():
  fields = [
    '{{c1::Berlin}} is the capital of {{c2::Germany}}',
    '{{c3::Paris}} is the capital of {{c4::France}}']

  note = Note(model=MULTI_FIELD_CLOZE_MODEL, fields=fields)
  assert sorted(card.ord for card in note.cards) == [0, 1, 2, 3]


def test_cloze_indicies_do_not_start_at_1():
  fields = ['{{c2::Mitochondria}} are the {{c3::powerhouses}} of the cell', '']
  note = Note(model=MY_CLOZE_MODEL, fields=fields)
  assert sorted(card.ord for card in note.cards) == [1, 2]


def test_cloze_newlines_in_deletion():
  fields = ['{{c1::Washington, D.C.}} is the capital of {{c2::the\nUnited States\nof America}}', '']
  note = Note(model=MY_CLOZE_MODEL, fields=fields)
  assert sorted(card.ord for card in note.cards) == [0, 1]


if __name__ == '__main__':
  test_cloze(len(sys.argv) != 1)
