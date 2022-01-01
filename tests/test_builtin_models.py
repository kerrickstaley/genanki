import genanki
import os
import pytest
import tempfile
import warnings


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

  with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    my_deck.add_note(genanki.Note(
      model=genanki.CLOZE_MODEL,
      fields=['{{c1::Rome}} is the capital of {{c2::Italy}}']))

  with warnings.catch_warnings(record=True) as warning_list:
    my_deck.add_note(genanki.Note(
      model=genanki.CLOZE_WITH_EXTRA_MODEL,
      fields=[
        '{{c1::Ottawa}} is the capital of {{c2::Canada}}',
        'Ottawa is in Ontario province.']))

  assert not warning_list

  # Just try writing the note to a .apkg file; if there is no Exception, we assume things are good.
  fnode, fpath = tempfile.mkstemp()
  os.close(fnode)
  my_deck.write_to_file(fpath)

  os.unlink(fpath)

def test_cloze_model_warns():
  with pytest.warns(DeprecationWarning):
    my_note = genanki.Note(
      model=genanki.CLOZE_MODEL,
      fields=['{{c1::Rome}} is the capital of {{c2::Italy}}'])
