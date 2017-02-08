import json
import os
import random
import sqlite3
import tempfile
import time
import yaml
import zipfile

from .apkg_col import APKG_COL
from .apkg_schema import APKG_SCHEMA

MODEL_ID = 1425274727596


def _random_guid():
  # TODO we want a stable guid
  base91_table = [
      'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
      't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
      'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4',
      '5', '6', '7', '8', '9', '!', '#', '$', '%', '&', '(', ')', '*', '+', ',', '-', '.', '/', ':',
      ';', '<', '=', '>', '?', '@', '[', ']', '^', '_', '`', '{', '|', '}', '~']
  val = random.randrange(2 ** 64)
  rv_reversed = []
  while val > 0:
    rv_reversed.append(base91_table[val % 91])
    val //= 91

  return ''.join(reversed(rv_reversed))


class Card:
  def __init__(self, ord_):
    self.ord_ = ord_

  def write_to_db(self, cursor, now_ts, deck_id, note_id):
    cursor.execute('INSERT INTO cards VALUES(null,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);', (
        note_id,    # nid
        deck_id,    # did
        self.ord_,  # ord
        now_ts,     # mod
        -1,         # usn
        0,          # type (=0 for non-Cloze)
        0,          # queue
        0,          # due
        0,          # ivl
        0,          # factor
        0,          # reps
        0,          # lapses
        0,          # left
        0,          # odue
        0,          # odid
        0,          # flags
        "",         # data
    ))


class Note:
  def __init__(self, model, fields, sort_field=None, tags=None):
    self.model = model  # TODO use this
    self.fields = fields

    if sort_field:
      self.sort_field = sort_field
    else:
      # TODO this is probably wrong
      self.sort_field = fields[0]

    self.tags = tags or []
    self.cards = []

  def add_card(self, *args, **kwargs):
    if len(args) == 1 and not kwargs and isinstance(args[0], Card):
      self.cards.append(args[0])
    else:
      self.cards.append(Card(*args, **kwargs))

  def write_to_db(self, cursor, now_ts, deck_id):
    cursor.execute('INSERT INTO notes VALUES(null,?,?,?,?,?,?,?,?,?,?);', (
        _random_guid(),         # TODO guid
        MODEL_ID,               # mid
        now_ts,                 # mod
        -1,                     # usn
        self._format_tags(),    # TODO tags
        self._format_fields(),  # flds
        self.sort_field,        # sfld
        0,                      # csum, can be ignored
        0,                      # flags
        '',                     # data
    ))

    for card in self.cards:
      card.write_to_db(cursor, now_ts, deck_id, cursor.lastrowid)

  def _format_fields(self):
    return '\x1f'.join(self.fields)

  def _format_tags(self):
    return ' ' + ' '.join(self.tags) + ' '


class Deck:
  def __init__(self, deck_id=None, name=None, fields=None, templates=None, css=None):
    self.deck_id = deck_id
    self.name = name
    self.set_fields(fields)
    self.set_templates(templates)
    self.set_css(css)
    self.notes = []

  def add_note(self, note):
    self.notes.append(note)

  def set_fields(self, fields):
    if isinstance(fields, list):
      self.fields = fields
    elif isinstance(fields, str):
      self.fields = yaml.load(fields)
    else:
      self.fields = yaml.load(fields.read())

  def set_templates(self, templates):
    if isinstance(templates, list):
      self.templates = templates
    elif isinstance(templates, str):
      self.templates = yaml.load(templates)
    else:
      self.templates = yaml.load(templates.read())

  def set_css(self, css):
    if isinstance(css, str):
      self.css = css
    else:
      self.css = css.read()

  def write_to_db(self, cursor, now_ts):
    # a lot of this stuff is in the wrong place, deck ID is hardcoded
    for ord_, tmpl in enumerate(self.templates):
      tmpl['ord'] = ord_
      tmpl['bafmt'] = ''
      tmpl['bqfmt'] = ''
      tmpl['did'] = None  # TODO None works just fine here, but should it be self.deck_id?

    query = (APKG_COL
        .replace('NAME', json.dumps(self.name))
        .replace('CARDCSS', json.dumps(self.css))
        .replace('FLDS', json.dumps(self.fields))
        .replace('TMPLS', json.dumps(self.templates))
        .replace('DECKID', json.dumps(self.deck_id)))
    cursor.execute(query)

    for note in self.notes:
      note.write_to_db(cursor, now_ts, self.deck_id)


class Package:
  def __init__(self, deck_or_decks=None):
    if isinstance(deck_or_decks, Deck):
      self.decks = [deck_or_decks]
    else:
      self.decks = deck_or_decks

  def write_to_file(self, file):
    dbfile, dbfilename = tempfile.mkstemp()
    os.close(dbfile)

    conn = sqlite3.connect(dbfilename)
    cursor = conn.cursor()

    now_ts = int(time.time())
    self.write_to_db(cursor, now_ts)

    conn.commit()
    conn.close()

    with zipfile.ZipFile(file, 'w') as outzip:
      outzip.write(dbfilename, 'collection.anki2')
      outzip.writestr('media', '{}')

  def write_to_db(self, cursor, now_ts):
    cursor.executescript(APKG_SCHEMA)

    for deck in self.decks:
      deck.write_to_db(cursor, now_ts)
