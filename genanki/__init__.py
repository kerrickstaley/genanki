from cached_property import cached_property
from copy import copy
from datetime import datetime
import hashlib
import json
import os
import pystache
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

  @cached_property
  def _req(self):
    """
    List of required fields for each template. Format is [tmpl_idx, "all"|"any", [req_field_1, req_field_2, ...]].

    Partial reimplementation of req computing logic from Anki. We use pystache instead of Anki's custom mustache
    implementation.

    The goal is to figure out which fields are "required", i.e. if they are missing then the front side of the note
    doesn't contain any meaningful content.
    """
    sentinel = 'SeNtInEl'
    field_names = [field['name'] for field in self.fields]

    req = []
    for template_ord, template in enumerate(self.templates):
      field_values = {field: sentinel for field in field_names}
      required_fields = []
      for field_ord, field in enumerate(field_names):
        fvcopy = copy(field_values)
        fvcopy[field] = ''

        rendered = pystache.render(template['qfmt'], fvcopy)

        if sentinel not in rendered:
          # when this field is missing, there is no meaningful content (no field values) in the question, so this field
          # is required
          required_fields.append(field_ord)

      if required_fields:
        req.append([template_ord, 'all', required_fields])
        continue

      # there are no required fields, so an "all" is not appropriate, switch to checking for "any"
      field_values = {field: '' for field in field_names}
      for field_ord, field in enumerate(field_names):
        fvcopy = copy(field_values)
        fvcopy[field] = sentinel

        rendered = pystache.render(template['qfmt'], fvcopy)

        if sentinel in rendered:
          # when this field is present, there is meaningful content in the question
          required_fields.append(field_ord)

      if not required_fields:
        raise Exception(
          'Could not compute required fields for this template; please check the formatting of "qfmt": {}'.format(
            template))

      req.append([template_ord, 'any', required_fields])

    return req

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
      "req": self._req,
      "sortf": 0,
      "tags": [],
      "tmpls": self.templates,
      "type": 0,
      "usn": -1,
      "vers": []
    }


class Card:
  def __init__(self, ord_):
    self.ord = ord_

    self.interval = 0

  def write_to_db(self, cursor, now_ts, deck_id, note_id,
                  level, due, interval, ease, reps_til_grad):
    cursor.execute('INSERT INTO cards VALUES(null,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);', (
        note_id,    # nid - note ID
        deck_id,    # did - deck ID
        self.ord,   # ord - which card template it corresponds
        now_ts,     # mod - modification time as epoch seconds
        -1,         # usn - value of -1 indicates need to push to server
        level,      # type - 0=new, 1=learning, 2=review
        level,      # queue - same as type unless buried
        due,        # due - new: unused
                    #       learning: due time as integer seconds since epoch
                    #       review: integer days relative to deck creation
        interval,   # ivl - positive days, negative seconds
        ease,       # factor - integer ease factor used by SRS, 2500 = 250%
        0,          # reps - number of reviews
        0,          # lapses - # times card went from "answered correctly" to "answered incorrectly"
     reps_til_grad, # left - reps left until graduation
        0,          # odue - only used when card is in filtered deck
        0,          # odid - only used when card is in filtered deck
        0,          # flags - currently unused
        "",         # data - currently unused
    ))


class Note:
  def __init__(self, model=None, fields=None, sort_field=None, tags=None, guid=None):
    self.model = model
    self.fields = fields
    self.sort_field = sort_field
    self.tags = tags or []
    try:
      self.guid = guid
    except AttributeError:
      # guid was defined as a property
      pass

    self.level = 0
    self.due = 0
    self.interval = 0
    self.ease = 1000
    self.reps_til_grad = 0

  @property
  def sort_field(self):
    return self._sort_field or self.fields[0]

  @sort_field.setter
  def sort_field(self, val):
    self._sort_field = val

  # We use cached_property instead of initializing in the constructor so that the user can set the model after calling
  # __init__ and it'll still work.
  @cached_property
  def cards(self):
    rv = []
    for card_ord, any_or_all, required_field_ords in self.model._req:
      op = {'any': any, 'all': all}[any_or_all]
      if op(self.fields[ord_] for ord_ in required_field_ords):
        rv.append(Card(card_ord))
    return rv

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

    note_id = cursor.lastrowid
    for card in self.cards:
      card.write_to_db(cursor, now_ts, deck_id, note_id,
                       self.level, self.due, self.interval,
                       self.ease, self.reps_til_grad)

  def _format_fields(self):
    return '\x1f'.join(self.fields)

  def _format_tags(self):
    return ' ' + ' '.join(self.tags) + ' '


class OptionsGroup:
  def __init__(self, options_id=1, name='Default'):
    self.options_id = options_id
    self.options_group_name = name
    #   General.
    self.max_time_per_answer = 60
    self.show_timer = False
    self.autoplay_audio = True
    self.replay_audio_for_answer = True
    #   New.
    self.new_steps = [1, 10]
    self.order = 1
    self.new_cardsperday = 20
    self.graduating_interval = 1
    self.easy_interval = 4
    self.starting_ease = 2500
    self.new_bury_related_cards = True
    #   Reviews.
    self.max_reviews_per_day = 100
    self.easy_bonus = 1.3
    self.interval_modifier = 1
    self.max_interval = 36500
    self.review_bury_related_cards = True
    #   Lapses.
    self.lapse_steps = [10]
    self.leech_interval_multiplier = 0
    self.lapse_min_interval = 1
    self.leech_threshold = 8
    self.leech_action = 0

    # Used for adding arbitrary options via JSON string. Useful for
    # addons.
    self.misc = ''

  def validate(self):
    if self.misc and self.misc[-1] != ',':
      self.misc += ','

  def _format_fields(self):
    self.validate()
    fields = {}
    for key, value in self.__dict__.items():
      if key.startswith('__') or callable(key):
        continue
      if type(value) is bool:
        fields[key] = str(value).lower()
      else:
        fields[key] = str(value)
    return fields


class Deck:
  def __init__(self, deck_id=None, name=None, options=None):
    self.deck_id = deck_id
    self.name = name
    self.notes = []
    self.models = {}  # map of model id to model
    self.description = ''
    self.options = options
    self.creation_time = datetime.now()

  def add_note(self, note):
    self.notes.append(note)

  def add_model(self, model):
    self.models[model.model_id] = model

  def write_to_db(self, cursor, now_ts):
    for note in self.notes:
      self.add_model(note.model)
    models = {model.model_id: model.to_json(now_ts, self.deck_id) for model in self.models.values()}

    params = self.options._format_fields()

    params.update({
      'creation_time': self.creation_time.timestamp(),
      'modification_time': self.creation_time.timestamp() * 1000,
      'name': self.name,
      'deck_id': self.deck_id,
      'models': json.dumps(models),
      'description': self.description,
    })

    cursor.execute(APKG_COL, params)

    for note in self.notes:
      note.write_to_db(cursor, now_ts, self.deck_id)

  def write_to_file(self, file):
    """
    Write this deck to a .apkg file.
    """
    Package(self).write_to_file(file)


class Package:
  def __init__(self, deck_or_decks=None, media_files=None):
    if isinstance(deck_or_decks, Deck):
      self.decks = [deck_or_decks]
    else:
      self.decks = deck_or_decks

    self.media_files = media_files or []

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

      media_json = dict(enumerate(self.media_files))
      outzip.writestr('media', json.dumps(media_json))

      for i, f in media_json.items():
        outzip.write(f, str(i))

  def write_to_db(self, cursor, now_ts):
    cursor.executescript(APKG_SCHEMA)

    for deck in self.decks:
      deck.write_to_db(cursor, now_ts)
