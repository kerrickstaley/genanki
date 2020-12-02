import itertools
import json
import os
import sqlite3
import tempfile
import time
import zipfile

from .apkg_col import APKG_COL
from .apkg_schema import APKG_SCHEMA
from .deck import Deck

from typing import Optional

class Package:
  def __init__(self, deck_or_decks=None, media_files=None):
    if isinstance(deck_or_decks, Deck):
      self.decks = [deck_or_decks]
    else:
      self.decks = deck_or_decks

    self.media_files = media_files or []

  def write_to_file(self, file, timestamp: Optional[float] = None):
    """
    :param file: File path to write to.
    :param timestamp: Timestamp (float seconds since Unix epoch) to assign to generated notes/cards. Can be used to
        make build hermetic. Defaults to time.time().
    """
    dbfile, dbfilename = tempfile.mkstemp()
    os.close(dbfile)

    conn = sqlite3.connect(dbfilename)
    cursor = conn.cursor()

    if timestamp is None:
      timestamp = time.time()

    id_gen = itertools.count(int(timestamp * 1000))
    self.write_to_db(cursor, timestamp, id_gen)

    conn.commit()
    conn.close()

    with zipfile.ZipFile(file, 'w') as outzip:
      outzip.write(dbfilename, 'collection.anki2')

      media_file_idx_to_path = dict(enumerate(self.media_files))
      media_json = {idx: os.path.basename(path) for idx, path in media_file_idx_to_path.items()}
      outzip.writestr('media', json.dumps(media_json))

      for idx, path in media_file_idx_to_path.items():
        outzip.write(path, str(idx))

  def write_to_db(self, cursor, timestamp: float, id_gen):
    cursor.executescript(APKG_SCHEMA)
    cursor.executescript(APKG_COL)

    for deck in self.decks:
      deck.write_to_db(cursor, timestamp, id_gen)

  def write_to_collection_from_addon(self):
    """
    Write to local collection. *Only usable when running inside an Anki addon!* Only tested on Anki 2.1.

    This writes to a temporary file and then calls the code that Anki uses to import packages.

    Note: the caller may want to use mw.checkpoint and mw.reset as follows:

      # creates a menu item called "Undo Add Notes From MyAddon" after this runs
      mw.checkpoint('Add Notes From MyAddon')
      # run import
      my_package.write_to_collection_from_addon()
      # refreshes main view so new deck is visible
      mw.reset()

    Tip: if your deck has the same name and ID as an existing deck, then the notes will get placed in that deck rather
    than a new deck being created.
    """
    from aqt import mw  # main window
    from anki.importing.apkg import AnkiPackageImporter

    tmpfilename = tempfile.NamedTemporaryFile(delete=False).name
    self.write_to_file(tmpfilename)
    AnkiPackageImporter(mw.col, tmpfilename).run()
