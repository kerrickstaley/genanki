import genanki
import os
import tempfile


def test_builtin_models():
  my_deck = genanki.Deck(
    1598559905,
    'Country Capitals')

  my_deck.add_note(genanki.Note(
    model=genanki.BASIC_MODEL,
    fields=['Capital of Argentina', 'Buenos Aires']))

  my_deck.add_note(genanki.Note(
    model=genanki.BASIC_AND_REVERSED_CARD_MODEL,
    fields=['Costa Rica', 'San José']))

  my_deck.add_note(genanki.Note(
    model=genanki.BASIC_OPTIONAL_REVERSED_CARD_MODEL,
    fields=['France', 'Paris', 'y']))

  my_deck.add_note(genanki.Note(
    model=genanki.BASIC_TYPE_IN_THE_ANSWER_MODEL,
    fields=['Taiwan', 'Taipei']))

  my_deck.add_note(genanki.Note(
    model=genanki.CLOZE_MODEL,
    fields=['{{c1::Rome}} is the capital of {{c2::Italy}}']))

  # Just try writing the note to a .apkg file; if there is no Exception, we assume things are good.
  fnode, fpath = tempfile.mkstemp()
  os.close(fnode)
  my_deck.write_to_file(fpath)

  os.unlink(fpath)
