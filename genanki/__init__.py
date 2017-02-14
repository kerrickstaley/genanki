import json
import hashlib
import os
import random
import sqlite3
import tempfile
import time
import yaml
import zipfile

from .apkg_col import APKG_COL
from .apkg_schema import APKG_SCHEMA

BASE91_TABLE = [
  'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
  't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
  'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4',
  '5', '6', '7', '8', '9', '!', '#', '$', '%', '&', '(', ')', '*', '+', ',', '-', '.', '/', ':',
  ';', '<', '=', '>', '?', '@', '[', ']', '^', '_', '`', '{', '|', '}', '~']


def guid_for(*values):
  hash_str = '__'.join(str(val) for val in values)

  # get the first 8 bytes of the SHA256 of hash_str as an int
  m = hashlib.sha256()
  m.update(hash_str.encode('utf-8'))
  hash_bytes = m.digest()[:8]
  hash_int = 0
  for b in hash_bytes:
    hash_int <<= 8
    hash_int += b

  # convert to the weird base91 format that Anki uses
  rv_reversed = []
  while hash_int > 0:
    rv_reversed.append(BASE91_TABLE[hash_int % 91])
    hash_int //= 91

  return ''.join(reversed(rv_reversed))


class Model:
  def __init__(self, model_id=None, name=None, fields=None, templates=None, css=''):
    self.model_id = model_id
    self.name = name
    self.set_fields(fields)
    self.set_templates(templates)
    self.css = css

  def set_fields(self, fields):
    if isinstance(fields, list):
      self.fields = fields
    elif isinstance(fields, str):
      self.fields = yaml.load(fields)

  def set_templates(self, templates):
    if isinstance(templates, list):
      self.templates = templates
    elif isinstance(templates, str):
      self.templates = yaml.load(templates)

  def to_json(self, now_ts, deck_id):
    for ord_, tmpl in enumerate(self.templates):
      tmpl['ord'] = ord_
      tmpl.setdefault('bafmt', '')
      tmpl.setdefault('bqfmt', '')
      tmpl.setdefault('did', None)  # TODO None works just fine here, but should it be deck_id?

    for ord_, field in enumerate(self.fields):
      field['ord'] = ord_
      field.setdefault('font', 'Liberation Sans')
      field.setdefault('media', [])
      field.setdefault('rtl', False)
      field.setdefault('size', 20)
      field.setdefault('sticky', False)

    # TODO: figure out how req works
    all_field_ords = list(range(len(self.fields)))
    req = [[tmpl_ord, "all", all_field_ords] for tmpl_ord in range(len(self.templates))]

    return {
      "css": self.css,
      "did": deck_id,
      "flds": self.fields,
      "id": str(self.model_id),
      "latexPost": "\\end{document}",
      "latexPre": "\\documentclass[12pt]{article}\n\\special{papersize=3in,5in}\n\\usepackage{amssymb,amsmath}\n"
                  "\\pagestyle{empty}\n\\setlength{\\parindent}{0in}\n\\begin{document}\n",
      "mod": now_ts,
      "name": self.name,
      "req": req,
      "sortf": 0,
      "tags": [],
      "tmpls": self.templates,
      "type": 0,
      "usn": -1,
      "vers": []
    }


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
  def __init__(self, model=None, fields=None, sort_field=None, tags=None, cards=None, guid=None):
    self.model = model
    self.fields = fields
    self.sort_field = sort_field
    self.tags = tags or []
    self.cards = cards
    self.guid = guid

  def add_card(self, *args, **kwargs):
    if len(args) == 1 and not kwargs and isinstance(args[0], Card):
      self.cards.append(args[0])
    else:
      self.cards.append(Card(*args, **kwargs))

  @property
  def sort_field(self):
    return self._sort_field or self.fields[0]

  @sort_field.setter
  def sort_field(self, val):
    self._sort_field = val

  @property
  def cards(self):
    if self._cards is None:
      return [Card(i) for i in range(len(self.model.templates))]
    return self._cards

  @cards.setter
  def cards(self, val):
    self._cards = val

  @property
  def guid(self):
    if self._guid is None:
      return guid_for(*self.fields)
    return self._guid

  @guid.setter
  def guid(self, val):
    self._guid = val

  def write_to_db(self, cursor, now_ts, deck_id):
    cursor.execute('INSERT INTO notes VALUES(null,?,?,?,?,?,?,?,?,?,?);', (
        self.guid,                    # guid
        self.model.model_id,          # mid
        now_ts,                       # mod
        -1,                           # usn
        self._format_tags(),          # TODO tags
        self._format_fields(),        # flds
        self.sort_field,              # sfld
        0,                            # csum, can be ignored
        0,                            # flags
        '',                           # data
    ))

    for card in self.cards:
      card.write_to_db(cursor, now_ts, deck_id, cursor.lastrowid)

  def _format_fields(self):
    return '\x1f'.join(self.fields)

  def _format_tags(self):
    return ' ' + ' '.join(self.tags) + ' '


class Deck:
  def __init__(self, deck_id=None, name=None):
    self.deck_id = deck_id
    self.name = name
    self.notes = []
    self.models = {}  # map of model id to model

  def add_note(self, note):
    self.notes.append(note)

  def add_model(self, model):
    self.models[model.model_id] = model

  def write_to_db(self, cursor, now_ts):
    for note in self.notes:
      self.add_model(note.model)
    models = {model.model_id: model.to_json(now_ts, self.deck_id) for model in self.models.values()}

    query = (APKG_COL
        .replace('NAME', json.dumps(self.name))
        .replace('DECKID', json.dumps(self.deck_id))
        .replace('MODELS', json.dumps(models)))
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
