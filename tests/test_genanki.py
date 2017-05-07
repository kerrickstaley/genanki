import os
import sys
sys.path.append(os.path.join(os.getcwd(), 'anki_upstream'))

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

TEST_MODEL_WITH_HINT = genanki.Model(
  456789, 'with hint',
  fields=[{'name': 'Question'}, {'name': 'Hint'}, {'name': 'Answer'}],
  templates=[
    {
      'name': 'card1',
      'qfmt': '{{Question}}'
              '{{#Hint}}<br>Hint: {{Hint}}{{/Hint}}',
      'afmt': '{{Answer}}',
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

  def import_package(self, pkg):
    """
    Imports `pkg` into self.col.

    :param genanki.Package pkg:
    """
    outf = tempfile.NamedTemporaryFile(suffix='.apkg', delete=False)
    outf.close()

    pkg.write_to_file(outf.name)

    importer = anki.importing.apkg.AnkiPackageImporter(self.col, outf.name)
    importer.run()

  def test_generated_deck_can_be_imported(self):
    deck = genanki.Deck(123456, 'foodeck')
    note = genanki.Note(TEST_MODEL, ['a', 'b'])
    deck.add_note(note)

    self.import_package(genanki.Package(deck))

    all_imported_decks = self.col.decks.all()
    assert len(all_imported_decks) == 2  # default deck and foodeck
    imported_deck = all_imported_decks[1]

    assert imported_deck['name'] == 'foodeck'

  def test_generated_deck_has_valid_cards(self):
    """
    Generates a deck with several notes and verifies that the nid/ord combinations on the generated cards make sense.

    Catches a bug that was fixed in 08d8a139.
    """
    deck = genanki.Deck(123456, 'foodeck')
    deck.add_note(genanki.Note(TEST_CN_MODEL, ['a', 'b', 'c']))  # 2 cards
    deck.add_note(genanki.Note(TEST_CN_MODEL, ['d', 'e', 'f']))  # 2 cards
    deck.add_note(genanki.Note(TEST_CN_MODEL, ['g', 'h', 'i']))  # 2 cards

    self.import_package(genanki.Package(deck))

    cards = [self.col.getCard(i) for i in self.col.findCards('')]

    # the bug causes us to fail to generate certain cards (e.g. the second card for the second note)
    assert len(cards) == 6

  def test_card_isEmpty__with_2_fields__succeeds(self):
    """Tests for a bug in an early version of genanki where notes with <4 fields were not supported."""
    deck = genanki.Deck(123456, 'foodeck')
    note = genanki.Note(TEST_MODEL, ['a', 'b'])
    deck.add_note(note)

    self.import_package(genanki.Package(deck))

    anki_note = self.col.getNote(self.col.findNotes('')[0])
    anki_card = anki_note.cards()[0]

    # test passes if this doesn't raise an exception
    anki_card.isEmpty()

  def test_Model_req(self):
    assert TEST_MODEL._req == [[0, 'all', [0]]]

  def test_Model_req__cn(self):
    assert TEST_CN_MODEL._req == [[0, 'all', [0]], [1, 'all', [1]]]

  def test_Model_req__with_hint(self):
    assert TEST_MODEL_WITH_HINT._req == [[0, 'any', [0, 1]]]

  def test_notes_generate_cards_based_on_req__cn(self):
    # has 'Simplified' field, will generate a 'Simplified' card
    n1 = genanki.Note(model=TEST_CN_MODEL, fields=['中國', '中国', 'China'])
    # no 'Simplified' field, so it won't generate a 'Simplified' card
    n2 = genanki.Note(model=TEST_CN_MODEL, fields=['你好', '', 'hello'])

    assert len(n1.cards) == 2
    assert n1.cards[0].ord == 0
    assert n1.cards[1].ord == 1

    assert len(n2.cards) == 1
    assert n2.cards[0].ord == 0

  def test_notes_generate_cards_based_on_req__with_hint(self):
    # both of these notes will generate one card
    n1 = genanki.Note(model=TEST_MODEL_WITH_HINT, fields=['capital of California', '', 'Sacramento'])
    n2 = genanki.Note(model=TEST_MODEL_WITH_HINT, fields=['capital of Iowa', 'French for "The Moines"', 'Des Moines'])

    assert len(n1.cards) == 1
    assert n1.cards[0].ord == 0
    assert len(n2.cards) == 1
    assert n2.cards[0].ord == 0

  def test_Note_with_guid_property(self):
    class MyNote(genanki.Note):
      @property
      def guid(self):
        return '3'

    # test passes if this doesn't raise an exception
    MyNote()
