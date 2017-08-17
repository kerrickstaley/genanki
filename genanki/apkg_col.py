APKG_COL = r'''
INSERT INTO col VALUES(
    null,
    1411124400,
    1425279151694,
    1425279151690,
    11,
    0,
    0,
    0,
    '{
        "activeDecks": [
            1
        ],
        "addToCur": true,
        "collapseTime": 1200,
        "curDeck": 1,
        "curModel": "1425279151691",
        "dueCounts": true,
        "estTimes": true,
        "newBury": true,
        "newSpread": 0,
        "nextPos": 1,
        "sortBackwards": false,
        "sortType": "noteFld",
        "timeLim": 0
    }',
    :models,
    '{
        "1": {
            "collapsed": false,
            "conf": 1,
            "desc": "",
            "dyn": 0,
            "extendNew": 10,
            "extendRev": 50,
            "id": 1,
            "lrnToday": [
                0,
                0
            ],
            "mod": 1425279151,
            "name": "Default",
            "newToday": [
                0,
                0
            ],
            "revToday": [
                0,
                0
            ],
            "timeToday": [
                0,
                0
            ],
            "usn": 0
        },
        "' || :deck_id || '": {
            "collapsed": false,
            "conf": ' || :options_id || ',
            "desc": "' || :description || '",
            "dyn": 0,
            "extendNew": 10,
            "extendRev": 50,
            "id": ' || :deck_id || ',
            "lrnToday": [
                5,
                0
            ],
            "mod": 1425278051,
            "name": "' || :name || '",
            "newToday": [
                5,
                0
            ],
            "revToday": [
                5,
                0
            ],
            "timeToday": [
                5,
                0
            ],
            "usn": -1
        }
    }',
    '{
        "' || :options_id || '": {
            "autoplay": ' || :autoplay_audio || ',
            "id": ' || :options_id || ',
            "lapse": {
                "delays": ' || :lapse_steps || ',
                "leechAction": ' || :leech_action || ',
                "leechFails": ' || :leech_threshold || ',
                "minInt": ' || :lapse_min_interval || ',
                "mult": ' || :leech_interval_multiplier || '
            },
            "maxTaken": ' || :max_time_per_answer || ',
            "mod": 0,
            "name": "' || :options_group_name || '",
            "new": {
                "bury": ' || :new_bury_related_cards || ',
                "delays": ' || :new_steps || ',
                "initialFactor": ' || :starting_ease || ',
                "ints": [
                    ' || :graduating_interval || ',
                    ' || :easy_interval || ',
                    7
                ],
                "order": ' || :order || ',
                "perDay": ' || :new_cardsperday || ',
                "separate": true
            },
            "replayq": ' || :replay_audio_for_answer || ',
            "rev": {
                "bury": ' || :review_bury_related_cards || ',
                "ease4": ' || :easy_bonus || ',
                "fuzz": 0.05,
                "ivlFct": ' || :interval_modifier || ',
                "maxIvl": ' || :max_interval || ',
                "minSpace": 1,
                "perDay": ' || :max_reviews_per_day || '
            },
            "timer": ' || :show_timer || ',
            "usn": 0
        }
    }',
    '{}'
);
'''
