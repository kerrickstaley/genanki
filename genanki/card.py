class Card:
  def __init__(self, ord, suspend=False):
    self.ord = ord
    self.suspend = suspend

  def write_to_db(self, cursor, timestamp: float, deck_id, note_id, id_gen, due=0):
    queue = -1 if self.suspend else 0
    cursor.execute('INSERT INTO cards VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);', (
        next(id_gen),    # id
        note_id,         # nid
        deck_id,         # did
        self.ord,        # ord
        int(timestamp),  # mod
        -1,              # usn
        0,               # type (=0 for non-Cloze)
        queue,           # queue
        due,             # due
        0,               # ivl
        0,               # factor
        0,               # reps
        0,               # lapses
        0,               # left
        0,               # odue
        0,               # odid
        0,               # flags
        "",              # data
    ))
