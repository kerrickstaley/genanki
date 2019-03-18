
import json

from .apkg_schema import APKG_SCHEMA
from .apkg_col import (
  ID,
  CRT,
  MOD,
  SCM,
  VER,
  DTY,
  USN,
  LS,
  CONF,
  MODELS,
  DECKS,
  DCONF,
  TAGS,
)

def init_db(cursor):
  cursor.executescript(APKG_SCHEMA)
  cursor.execute(
    'INSERT INTO col '
    '(id, crt, mod, scm, ver, dty, usn, ls, conf, models, decks, dconf, tags) '
    'VALUES '
    '(?,  ?,   ?,   ?,   ?,   ?,   ?,   ?,  ?,    ?,      ?,     ?,     ?   );',
    (
      ID, CRT, MOD, SCM, VER, DTY, USN, LS, CONF, MODELS, DECKS, DCONF, TAGS
    )
  )

def add_deck(cursor, deck):
  decks_json, = cursor.execute('SELECT decks FROM col').fetchone()
  if not decks_json:
    raise RuntimeError('Database does not contain any deck')

  decks = json.loads(decks_json)
  decks[str(deck.deck_id)] = deck.to_dict()

  new_decks_json = json.dumps(decks)
  cursor.execute('UPDATE col SET decks = ?', (new_decks_json,))

def add_model(cursor, model, deck_id):
  models_json, = cursor.execute('SELECT models FROM col').fetchone()
  assert models_json is not None

  models = json.loads(models_json)
  models[str(model.id)] = model.to_dict(deck_id)

  new_models_json = json.dumps(models)
  cursor.execute('UPDATE col SET models = ?', (new_models_json,))

def add_note(cursor, note):
  pass

def add_card(cursor, card):
  pass
