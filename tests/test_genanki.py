import sys
sys.path.append('/usr/share/anki')

import tempfile

import anki
import anki.importing.apkg

import genanki

TEST_MODEL = genanki.Model(
  234567, 'foomodel',
  fields=[
    {
      'name': 'AField',
    },
    {
      'name': 'BField',
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
)

TEST_CN_MODEL = genanki.Model(
  345678, 'Chinese',
  fields=[{'name': 'Traditional'}, {'name': 'Simplified'}, {'name': 'English'}],
  templates=[
    {
      'name': 'Traditional',
      'qfmt': '{{Traditional}}',
      'afmt': '{{FrontSide}}'
              '<hr id="answer">'
              '{{English}}',
    },
    {
      'name': 'Simplified',
      'qfmt': '{{Simplified}}',
      'afmt': '{{FrontSide}}'
              '<hr id="answer">'
              '{{English}}',
    },
  ],
)


class TestWithCollection:
  def setup(self):
    # TODO make this less messy
    colf = tempfile.NamedTemporaryFile(suffix='.anki2')
    colf_name = colf.name
    colf.close()  # colf is deleted
    self.col = anki.Collection(colf_name)

  def test_generated_deck_can_be_imported(self):
    deck = genanki.Deck(123456, 'foodeck')
    note = genanki.Note(TEST_MODEL, ['a', 'b'])
    deck.add_note(note)

    outf = tempfile.NamedTemporaryFile(suffix='.apkg', delete=False)
    outf.close()

    genanki.Package(deck).write_to_file(outf.name)

    importer = anki.importing.apkg.AnkiPackageImporter(self.col, outf.name)
    importer.run()

    all_imported_decks = self.col.decks.all()
    assert len(all_imported_decks) == 2  # default deck and foodeck
    imported_deck = all_imported_decks[1]

    assert imported_deck['name'] == 'foodeck'

  def test_card_isEmpty__with_2_fields__succeeds(self):
    """Tests for a bug in an early version of genanki where notes with <4 fields were not supported."""
    deck = genanki.Deck(123456, 'foodeck')
    note = genanki.Note(TEST_MODEL, ['a', 'b'])
    deck.add_note(note)

    outf = tempfile.NamedTemporaryFile(suffix='.apkg', delete=False)
    outf.close()

    genanki.Package(deck).write_to_file(outf.name)

    importer = anki.importing.apkg.AnkiPackageImporter(self.col, outf.name)
    importer.run()

    anki_note = self.col.getNote(self.col.findNotes('')[0])
    anki_card = anki_note.cards()[0]

    # test passes if this doesn't raise an exception
    anki_card.isEmpty()

  def test_Model_req(self):
    assert TEST_MODEL._req == [[0, 'all', [0]]]

  def test_Model_req__cn(self):
    assert TEST_CN_MODEL._req == [[0, 'all', [0]], [1, 'all', [1]]]

  def test_notes_generate_cards_based_on_req(self):
    # has 'Simplified' field, will generate a 'Simplified' card
    n1 = genanki.Note(model=TEST_CN_MODEL, fields=['中國', '中国', 'China'])
    # no 'Simplified' field, so it won't generate a 'Simplified' card
    n2 = genanki.Note(model=TEST_CN_MODEL, fields=['你好', '', 'hello'])

    assert len(n1.cards) == 2
    assert n1.cards[0].ord == 0
    assert n1.cards[1].ord == 1

    assert len(n2.cards) == 1
    assert n2.cards[0].ord == 0
