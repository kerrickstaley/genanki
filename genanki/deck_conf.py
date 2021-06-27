
import copy
import json


DEFAULT_CONF = {
    "autoplay": True,
    "id": 1,
    "lapse": {
        "delays": [
            10
        ],
        "leechAction": 0,
        "leechFails": 8,
        "minInt": 1,
        "mult": 0
    },
    "maxTaken": 60,
    "mod": 0,
    "name": "Default",
    "new": {
        "bury": True,
        "delays": [
            1,
            10
        ],
        "initialFactor": 2500,
        "ints": [
            1,
            4,
            7
        ],
        "order": 1,
        "perDay": 20,
        "separate": True
    },
    "replayq": True,
    "rev": {
        "bury": True,
        "ease4": 1.3,
        "fuzz": 0.05,
        "ivlFct": 1,
        "maxIvl": 36500,
        "minSpace": 1,
        "perDay": 100
    },
    "timer": 0,
    "usn": 0
}


class DeckConf:
  def __init__(self, deck_conf_id, name, conf=None):
    self.deck_conf_id = deck_conf_id
    self.name = name
    conf = copy.deepcopy(DEFAULT_CONF) if conf is None else conf
    conf["name"] = self.name
    conf["id"] = self.deck_conf_id
    self.conf = conf

  def to_json(self):
    return self.conf

  def write_to_db(self, cursor, timestamp):
    conf_json_str, = cursor.execute('SELECT dconf FROM col').fetchone()
    confs = json.loads(conf_json_str)
    confs.update({str(self.deck_conf_id): self.to_json()})
    cursor.execute('UPDATE col SET dconf = ?', (json.dumps(confs),))
