import os
import sys
sys.path.append(os.path.join(os.getcwd(), 'anki_upstream'))

import pytest
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

# Same as default latex_pre but we include amsfonts package
CUSTOM_LATEX_PRE = ('\\documentclass[12pt]{article}\n\\special{papersize=3in,5in}\n\\usepackage[utf8]{inputenc}\n'
                    + '\\usepackage{amssymb,amsmath,amsfonts}\n\\pagestyle{empty}\n\\setlength{\\parindent}{0in}\n'
                    + '\\begin{document}\n')
# Same as default latex_post but we add a comment. (What is a real-world use-case for customizing latex_post?)
CUSTOM_LATEX_POST = '% here is a great comment\n\\end{document}'

TEST_MODEL_WITH_LATEX = genanki.Model(
  567890, 'with latex',
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
  latex_pre=CUSTOM_LATEX_PRE,
  latex_post=CUSTOM_LATEX_POST,
)

CUSTOM_SORT_FIELD_INDEX = 1  # Anki default value is 0
TEST_MODEL_WITH_SORT_FIELD_INDEX = genanki.Model(
  987123, 'with sort field index',
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
  sort_field_index=CUSTOM_SORT_FIELD_INDEX,
)

# VALID_MP3 and VALID_JPG courtesy of https://github.com/mathiasbynens/small
VALID_MP3 = (
  b'\xff\xe3\x18\xc4\x00\x00\x00\x03H\x00\x00\x00\x00LAME3.98.2\x00\x00\x00'
  b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
  b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
  b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')

VALID_JPG = (
  b'\xff\xd8\xff\xdb\x00C\x00\x03\x02\x02\x02\x02\x02\x03\x02\x02\x02\x03\x03'
  b'\x03\x03\x04\x06\x04\x04\x04\x04\x04\x08\x06\x06\x05\x06\t\x08\n\n\t\x08\t'
  b'\t\n\x0c\x0f\x0c\n\x0b\x0e\x0b\t\t\r\x11\r\x0e\x0f\x10\x10\x11\x10\n\x0c'
  b'\x12\x13\x12\x10\x13\x0f\x10\x10\x10\xff\xc9\x00\x0b\x08\x00\x01\x00\x01'
  b'\x01\x01\x11\x00\xff\xcc\x00\x06\x00\x10\x10\x05\xff\xda\x00\x08\x01\x01'
  b'\x00\x00?\x00\xd2\xcf \xff\xd9')


class TestWithCollection:
  def setup_method(self):
    # TODO make this less messy
    colf = tempfile.NamedTemporaryFile(suffix='.anki2')
    colf_name = colf.name
    colf.close()  # colf is deleted
    self.col = anki.Collection(colf_name)

  def import_package(self, pkg, timestamp=None):
    """
    Imports `pkg` into self.col.

    :param genanki.Package pkg:
    """
    outf = tempfile.NamedTemporaryFile(suffix='.apkg', delete=False)
    outf.close()

    pkg.write_to_file(outf.name, timestamp=timestamp)

    importer = anki.importing.apkg.AnkiPackageImporter(self.col, outf.name)
    importer.run()

  def check_media(self):
    # col.media.check seems to assume that the cwd is the media directory. So this helper function
    # chdirs to the media dir before running check and then goes back to the original cwd.
    orig_cwd = os.getcwd()
    os.chdir(self.col.media.dir())
    ret = self.col.media.check()
    os.chdir(orig_cwd)
    return ret

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

  def test_multi_deck_package(self):
    deck1 = genanki.Deck(123456, 'foodeck')
    deck2 = genanki.Deck(654321, 'bardeck')

    note = genanki.Note(TEST_MODEL, ['a', 'b'])

    deck1.add_note(note)
    deck2.add_note(note)

    self.import_package(genanki.Package([deck1, deck2]))

    all_imported_decks = self.col.decks.all()
    assert len(all_imported_decks) == 3  # default deck, foodeck, and bardeck

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

  def test_media_files(self):
    # change to a scratch directory so we can write files
    os.chdir(tempfile.mkdtemp())

    deck = genanki.Deck(123456, 'foodeck')
    note = genanki.Note(TEST_MODEL, [
      'question [sound:present.mp3] [sound:missing.mp3]',
      'answer <img src="present.jpg"> <img src="missing.jpg">'])
    deck.add_note(note)

    # populate files with data
    with open('present.mp3', 'wb') as h:
      h.write(VALID_MP3)
    with open('present.jpg', 'wb') as h:
      h.write(VALID_JPG)

    package = genanki.Package(deck, media_files=['present.mp3', 'present.jpg'])
    self.import_package(package)

    os.remove('present.mp3')
    os.remove('present.jpg')

    missing, unused, invalid = self.check_media()
    assert set(missing) == {'missing.mp3', 'missing.jpg'}

  def test_media_files_in_subdirs(self):
    # change to a scratch directory so we can write files
    os.chdir(tempfile.mkdtemp())

    deck = genanki.Deck(123456, 'foodeck')
    note = genanki.Note(TEST_MODEL, [
      'question [sound:present.mp3] [sound:missing.mp3]',
      'answer <img src="present.jpg"> <img src="missing.jpg">'])
    deck.add_note(note)

    # populate files with data
    os.mkdir('subdir1')
    with open('subdir1/present.mp3', 'wb') as h:
      h.write(VALID_MP3)
    os.mkdir('subdir2')
    with open('subdir2/present.jpg', 'wb') as h:
      h.write(VALID_JPG)

    package = genanki.Package(deck, media_files=['subdir1/present.mp3', 'subdir2/present.jpg'])
    self.import_package(package)

    os.remove('subdir1/present.mp3')
    os.remove('subdir2/present.jpg')

    missing, unused, invalid = self.check_media()
    assert set(missing) == {'missing.mp3', 'missing.jpg'}

  def test_media_files_absolute_paths(self):
    # change to a scratch directory so we can write files
    os.chdir(tempfile.mkdtemp())
    media_dir = tempfile.mkdtemp()

    deck = genanki.Deck(123456, 'foodeck')
    note = genanki.Note(TEST_MODEL, [
      'question [sound:present.mp3] [sound:missing.mp3]',
      'answer <img src="present.jpg"> <img src="missing.jpg">'])
    deck.add_note(note)

    # populate files with data
    present_mp3_path = os.path.join(media_dir, 'present.mp3')
    present_jpg_path = os.path.join(media_dir, 'present.jpg')
    with open(present_mp3_path, 'wb') as h:
      h.write(VALID_MP3)
    with open(present_jpg_path, 'wb') as h:
      h.write(VALID_JPG)

    package = genanki.Package(deck, media_files=[present_mp3_path, present_jpg_path])
    self.import_package(package)

    missing, unused, invalid = self.check_media()
    assert set(missing) == {'missing.mp3', 'missing.jpg'}

  def test_write_deck_without_deck_id_fails(self):
    # change to a scratch directory so we can write files
    os.chdir(tempfile.mkdtemp())

    deck = genanki.Deck()
    deck.name = 'foodeck'

    with pytest.raises(TypeError):
      deck.write_to_file('foodeck.apkg')

  def test_write_deck_without_name_fails(self):
    # change to a scratch directory so we can write files
    os.chdir(tempfile.mkdtemp())

    deck = genanki.Deck()
    deck.deck_id = 123456

    with pytest.raises(TypeError):
      deck.write_to_file('foodeck.apkg')

  def test_card_suspend(self):
    deck = genanki.Deck(123456, 'foodeck')
    note = genanki.Note(model=TEST_CN_MODEL, fields=['中國', '中国', 'China'])
    assert len(note.cards) == 2

    note.cards[1].suspend = True

    deck.add_note(note)

    self.import_package(genanki.Package(deck), timestamp=0)

    assert self.col.findCards('') == [1, 2]
    assert self.col.findCards('is:suspended') == [2]

  def test_deck_with_description(self):
    deck = genanki.Deck(112233, 'foodeck', description='This is my great deck.\nIt is so so great.')
    note = genanki.Note(TEST_MODEL, ['a', 'b'])
    deck.add_note(note)

    self.import_package(genanki.Package(deck))

    all_decks = self.col.decks.all()
    assert len(all_decks) == 2  # default deck and foodeck
    imported_deck = all_decks[1]

    assert imported_deck['desc'] == 'This is my great deck.\nIt is so so great.'

  def test_card_added_date_is_recent(self):
    """
    Checks for a bug where cards were assigned the creation date 1970-01-01 (i.e. the Unix epoch).

    See https://github.com/kerrickstaley/genanki/issues/29 .

    The "Added" date is encoded in the card.id field; see
    https://github.com/ankitects/anki/blob/ed8340a4e3a2006d6285d7adf9b136c735ba2085/anki/stats.py#L28

    TODO implement a fix so that this test passes.
    """
    deck = genanki.Deck(1104693946, 'foodeck')
    note = genanki.Note(TEST_MODEL, ['a', 'b'])
    deck.add_note(note)

    self.import_package(genanki.Package(deck))

    anki_note = self.col.getNote(self.col.findNotes('')[0])
    anki_card = anki_note.cards()[0]

    assert anki_card.id > 1577836800000  # Jan 1 2020 UTC (milliseconds since epoch)

  def test_model_with_latex_pre_and_post(self):
    deck = genanki.Deck(1681249286, 'foodeck')
    note = genanki.Note(TEST_MODEL_WITH_LATEX, ['a', 'b'])
    deck.add_note(note)

    self.import_package(genanki.Package(deck))

    anki_note = self.col.getNote(self.col.findNotes('')[0])
    assert anki_note.model()['latexPre'] == CUSTOM_LATEX_PRE
    assert anki_note.model()['latexPost'] == CUSTOM_LATEX_POST

  def test_model_with_sort_field_index(self):
      deck = genanki.Deck(332211, 'foodeck')
      note = genanki.Note(TEST_MODEL_WITH_SORT_FIELD_INDEX, ['a', '3.A'])
      deck.add_note(note)

      self.import_package(genanki.Package(deck))

      anki_note = self.col.getNote(self.col.findNotes('')[0])
      assert anki_note.model()['sortf'] == CUSTOM_SORT_FIELD_INDEX

  def test_notes_with_due1(self):
    deck = genanki.Deck(4145273926, 'foodeck')
    deck.add_note(genanki.Note(
      TEST_MODEL,
      ['Capital of Washington', 'Olympia'],
      due=1))
    deck.add_note(genanki.Note(
      TEST_MODEL,
      ['Capital of Oregon', 'Salem'],
      due=2))

    self.import_package(genanki.Package(deck))

    self.col.decks.select(self.col.decks.id('foodeck'))
    self.col.sched.reset()
    next_card = self.col.sched.getCard()
    next_note = self.col.getNote(next_card.nid)

    # Next card is the one with lowest due value.
    assert next_note.fields == ['Capital of Washington', 'Olympia']

  def test_notes_with_due2(self):
    # Same as test_notes_with_due1, but we switch the due values
    # for the two notes.
    deck = genanki.Deck(4145273927, 'foodeck')
    deck.add_note(genanki.Note(
      TEST_MODEL,
      ['Capital of Washington', 'Olympia'],
      due=2))
    deck.add_note(genanki.Note(
      TEST_MODEL,
      ['Capital of Oregon', 'Salem'],
      due=1))

    self.import_package(genanki.Package(deck))

    self.col.decks.select(self.col.decks.id('foodeck'))
    self.col.sched.reset()
    next_card = self.col.sched.getCard()
    next_note = self.col.getNote(next_card.nid)

    # Next card changes to "Capital of Oregon", because it has lower
    # due value.
    assert next_note.fields == ['Capital of Oregon', 'Salem']

  def test_deck_with_config(self):
    conf = genanki.DeckConf(666, 'MyConf')
    # Changing default initialFactor from 2500 to 4500
    conf.conf['new']['initialFactor'] = 4500
    deck = genanki.Deck(112233, 'foodeck', conf=conf)
    # The Anki importer need at least one card to import the config.
    # See related discussion:
    # https://anki.tenderapp.com/discussions/ankidesktop/38114-importing-apkg-does-not-update-deck-config-fields
    note = genanki.Note(TEST_MODEL, ['a', 'b'])
    deck.add_note(note)

    self.import_package(genanki.Package(deck))

    all_confs = self.col.decks.allConf()
    assert len(all_confs) == 2  # default conf and MyConf
    imported_deck = all_confs[1]

    assert imported_deck['new']['initialFactor'] == 4500

  def test_deck_with_2_config(self):
    conf = genanki.DeckConf(666, 'MyConf')
    conf.conf['new']['initialFactor'] = 4500
    deck = genanki.Deck(112233, 'foodeck', conf=conf)
    note = genanki.Note(TEST_MODEL, ['a', 'b'])
    deck.add_note(note)

    self.import_package(genanki.Package(deck))
    conf = genanki.DeckConf(6666, 'MyConf2')
    conf.conf['new']['initialFactor'] = 5500
    deck = genanki.Deck(11223344, 'boodeck', conf=conf)
    note = genanki.Note(TEST_MODEL, ['a', 'b'])
    deck.add_note(note)

    self.import_package(genanki.Package(deck))

    all_confs = self.col.decks.allConf()
    assert len(all_confs) == 2  # default conf and MyConf
    imported_deck = all_confs[1]

    assert imported_deck['new']['initialFactor'] == 4500
