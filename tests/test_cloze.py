"""Test creating Cloze cards"""

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

def test_cloze():
  """Test Cloze model"""
  notes = []
  assert MY_CLOZE_MODEL.to_json(0, 0)["type"] == 1

  fields = ['NOTE ONE: {{c1::single deletion}}', '']
  my_cloze_note = Note(model=MY_CLOZE_MODEL, fields=fields)
  assert {card.ord for card in my_cloze_note.cards} == {0}
  notes.append(my_cloze_note)

  fields = ['NOTE TWO: {{c1::1st deletion}} {{c2::2nd deletion}} {{c3::3rd deletion}}', '']
  my_cloze_note = Note(model=MY_CLOZE_MODEL, fields=fields)
  assert {card.ord for card in my_cloze_note.cards} == {0, 1, 2}
  notes.append(my_cloze_note)

  fields = ['NOTE THREE: {{c1::1st deletion::C1-CLOZE}}', '']
  my_cloze_note = Note(model=MY_CLOZE_MODEL, fields=fields)
  assert {card.ord for card in my_cloze_note.cards} == {0}
  notes.append(my_cloze_note)

  deckname = 'mtherieau'
  deck = Deck(deck_id=0, name=deckname)
  for note in notes:
    deck.add_note(note)
  fout_anki = '{NAME}.apkg'.format(NAME=deckname)
  Package(deck).write_to_file(fout_anki)
  print('  {N} WROTE: {APKG}'.format(N=len(notes), APKG=fout_anki))

if __name__ == '__main__':
  test_cloze()
