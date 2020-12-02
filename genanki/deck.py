import json

class Deck:
  def __init__(self, deck_id=None, name=None, description=''):
    self.deck_id = deck_id
    self.name = name
    self.description = description
    self.notes = []
    self.models = {}  # map of model id to model

  def add_note(self, note):
    self.notes.append(note)

  def add_model(self, model):
    self.models[model.model_id] = model

  def to_json(self):
    return {
      "collapsed": False,
      "conf": 1,
      "desc": self.description,
      "dyn": 0,
      "extendNew": 0,
      "extendRev": 50,
      "id": self.deck_id,
      "lrnToday": [
          163,
          2
      ],
      "mod": 1425278051,
      "name": self.name,
      "newToday": [
          163,
          2
      ],
      "revToday": [
          163,
          0
      ],
      "timeToday": [
          163,
          23598
      ],
      "usn": -1
    }

  def write_to_db(self, cursor, timestamp: float, id_gen):
    if not isinstance(self.deck_id, int):
      raise TypeError('Deck .deck_id must be an integer, not {}.'.format(self.deck_id))
    if not isinstance(self.name, str):
      raise TypeError('Deck .name must be a string, not {}.'.format(self.name))

    decks_json_str, = cursor.execute('SELECT decks FROM col').fetchone()
    decks = json.loads(decks_json_str)
    decks.update({str(self.deck_id): self.to_json()})
    cursor.execute('UPDATE col SET decks = ?', (json.dumps(decks),))

    models_json_str, = cursor.execute('SELECT models from col').fetchone()
    models = json.loads(models_json_str)
    for note in self.notes:
      self.add_model(note.model)
    models.update(
      {model.model_id: model.to_json(timestamp, self.deck_id) for model in self.models.values()})
    cursor.execute('UPDATE col SET models = ?', (json.dumps(models),))

    for note in self.notes:
      note.write_to_db(cursor, timestamp, self.deck_id, id_gen)

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
