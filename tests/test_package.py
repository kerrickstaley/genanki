import os
import tempfile

import pytest

import genanki


def _make_package():
  model = genanki.Model(
    1607392319,
    'Simple Model',
    fields=[{'name': 'Question'}, {'name': 'Answer'}],
    templates=[{'name': 'Card 1', 'qfmt': '{{Question}}', 'afmt': '{{Answer}}'}],
  )
  deck = genanki.Deck(2059400110, 'Country Capitals')
  deck.add_note(genanki.Note(model=model, fields=['Capital of Argentina', 'Buenos Aires']))
  return genanki.Package(deck)


@pytest.fixture
def private_tempdir(tmp_path, monkeypatch):
  """Point tempfile at an empty directory, so anything write_to_file leaves behind is visible."""
  scratch = tmp_path / 'tmp'
  scratch.mkdir()
  monkeypatch.setattr(tempfile, 'tempdir', str(scratch))
  return scratch


def test_write_to_file_removes_temporary_database(tmp_path, private_tempdir):
  out = tmp_path / 'deck.apkg'
  _make_package().write_to_file(str(out))

  assert out.exists()
  assert os.listdir(str(private_tempdir)) == []


def test_write_to_file_removes_temporary_database_when_writing_the_database_fails(tmp_path, private_tempdir):
  deck = genanki.Deck()
  deck.name = 'foodeck'  # no deck_id, so write_to_db raises

  with pytest.raises(TypeError):
    genanki.Package(deck).write_to_file(str(tmp_path / 'deck.apkg'))

  assert os.listdir(str(private_tempdir)) == []


def test_write_to_file_removes_temporary_database_when_zipping_fails(tmp_path, private_tempdir):
  pkg = _make_package()
  pkg.media_files = [str(tmp_path / 'missing.mp3')]

  with pytest.raises(FileNotFoundError):
    pkg.write_to_file(str(tmp_path / 'deck.apkg'))

  assert os.listdir(str(private_tempdir)) == []
