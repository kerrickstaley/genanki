class Card:
  def __init__(self, ord, suspend=False):
    self.ord = ord
    self.suspend = suspend

  def write_to_db(self, cursor, now_ts, deck_id, note_id):
    queue = -1 if self.suspend else 0
    cursor.execute('INSERT INTO cards VALUES(null,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);', (
        note_id,    # nid
        deck_id,    # did
        self.ord,   # ord
        now_ts,     # mod
        -1,         # usn
        0,          # type (=0 for non-Cloze)
        queue,      # queue
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
