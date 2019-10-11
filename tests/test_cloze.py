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

  # Question: NOTE FOUR: foo bar [...]
  # Answer:   NOTE FOUR: foo bar 3rd deletion
  fields = ['NOTE FOUR: {{c1:1st deletion}} foo {{c2:2nd deletion}} bar {{c1::3rd deletion}}', '']
  my_cloze_note = Note(model=MY_CLOZE_MODEL, fields=fields)
  assert {card.ord for card in my_cloze_note.cards} == {0}
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


if __name__ == '__main__':
  test_cloze(len(sys.argv) != 1)
