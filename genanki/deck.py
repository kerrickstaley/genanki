
import json

from . import db

class Deck:
  def __init__(self, id: int, name: str):
    self.id = id
    self.name = name
    self.notes = []
    self.models = {}  # map of model id to model

  def add_note(self, note):
    self.notes.append(note)

  def add_model(self, model):
    self.models[model.id] = model

  def update_models(self):
    for note in self.notes:
      self.add_model(note.model)

  def to_dict(self):
    return {
      'collapsed': True,
      'conf': 1,
      'desc': '',
      'dyn': 0,
      'extendNew': 0,
      'extendRev': 50,
      'id': self.id,
      'lrnToday': [
        163,
        2
      ],
      'mod': 1425278051,
      'name': self.name,
      'newToday': [
        163,
        2
      ],
      'revToday': [
          163,
          0
      ],
      'timeToday': [
        163,
        23598
      ],
      'usn': -1
    }

  def write_to_db(self, cursor, now_ts):
    self.update_models()

    for model in self.models.values():
      db.add_model(cursor, model, self.id)

    db.add_deck(cursor, self)

    for note in self.notes:
      note.write_to_db(cursor, now_ts, self.id)

  def write_to_file(self, file):
    """
    Write this deck to a .apkg file.
    """
    from .package import Package
    Package(self).write_to_file(file)

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
    from .package import Package
    Package(self).write_to_collection_from_addon()
