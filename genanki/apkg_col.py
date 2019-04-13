
import json

ID = None
CRT = 1411124400
MOD = 1425279151694
SCM = 1425279151690
VER = 11
DTY = 0
USN = 0
LS = 0

CONF_DICT = {
  'activeDecks': [
    1,
  ],
  'addToCur': True,
  'collapseTime': 1200,
  'curDeck': 1,
  'curModel': '1425279151691',
  'dueCounts': True,
  'estTimes': True,
  'newBury': True,
  'newSpread': 0,
  'nextPos': 1,
  'sortBackwards': False,
  'sortType': 'noteFld',
  'timeLim': 0,
}
CONF = json.dumps(CONF_DICT)

MODELS_DICT = {}
MODELS = json.dumps(MODELS_DICT)

DECKS_DICT = {
  '1': {
    'collapsed': False,
    'conf': 1,
    'desc': '',
    'dyn': 0,
    'extendNew': 10,
    'extendRev': 50,
    'id': 1,
    'lrnToday': [
      0,
      0
    ],
    'mod': 1425279151,
    'name': 'Default',
    'newToday': [
      0,
      0
    ],
    'revToday': [
      0,
      0
    ],
    'timeToday': [
      0,
      0
    ],
    'usn': 0
  }
}
DECKS = json.dumps(DECKS_DICT)

DCONF_DICT = {
  '1': {
    'autoplay': True,
    'id': 1,
    'lapse': {
      'delays': [
        10
      ],
      'leechAction': 0,
      'leechFails': 8,
      'minInt': 1,
      'mult': 0
    },
    'maxTaken': 60,
    'mod': 0,
    'name': 'Default',
    'new': {
      'bury': True,
      'delays': [
        1,
        10
      ],
      'initialFactor': 2500,
      'ints': [
        1,
        4,
        7
      ],
      'order': 1,
      'perDay': 20,
      'separate': True
    },
    'replayq': True,
    'rev': {
      'bury': True,
      'ease4': 1.3,
      'fuzz': 0.05,
      'ivlFct': 1,
      'maxIvl': 36500,
      'minSpace': 1,
      'perDay': 100
    },
    'timer': 0,
    'usn': 0
  }
}
DCONF = json.dumps(DCONF_DICT)

TAGS_DICT = {}
TAGS = json.dumps(TAGS_DICT)
