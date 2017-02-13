import sys
sys.path.append('/usr/share/anki')

import tempfile

import anki
import anki.importing.apkg

import genanki


class TestWithCollection:
  def setup(self):
    # TODO make this less messy
    colf = tempfile.NamedTemporaryFile(suffix='.anki2')
    colf_name = colf.name
    colf.close()  # colf is deleted
    self.col = anki.Collection(colf_name)

  def test_generated_deck_can_be_imported(self):
    deck = genanki.Deck(123456, 'foodeck')
    model = genanki.Model(
      234567, 'foomodel',
      fields=[
        {
          'font': 'Liberation Sans',
          'media': [],
          'name': 'AField',
          'ord': 0,
          'rtl': False,
          'size': 20,
          'sticky': False
        },
        {
          'font': 'Liberation Sans',
          'media': [],
          'name': 'BField',
          'ord': 1,
          'rtl': False,
          'size': 20,
          'sticky': False
        },
      ],
      templates=[
        {
          'name': 'card1',
          'qfmt': '{{AField}}',
          'afmt': '{{FrontSide}}'
                  '<hr id="answer">'
                  '{{BField}}',
        }
      ],
      css='',
    )
    note = genanki.Note(model, ['a', 'b'])
    note.add_card(0)
    deck.add_note(note)

    outf = tempfile.NamedTemporaryFile(delete=False)
    outf.close()

    genanki.Package(deck).write_to_file(outf.name)

    importer = anki.importing.apkg.AnkiPackageImporter(self.col, outf.name)
    importer.run()

    all_imported_decks = self.col.decks.all()
    assert len(all_imported_decks) == 2  # default deck and foodeck
    imported_deck = all_imported_decks[1]

    assert imported_deck['name'] == 'foodeck'
