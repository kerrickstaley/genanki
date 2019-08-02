import random

from .deck import Deck
from .note import Note
from .package import Package

from .models import simple_model


def get_random_id():
    return random.randrange(1 << 32)


def make_deck(cards, name):
    # Cards is a list of fields
    deck = Deck(get_random_id(), name)

    for card in cards:
        note = Note(
            model=simple_model,
            fields=card
        )
        deck.add_note(note)

    return deck


def write_decks(decks, name='output'):
    Package(decks).write_to_file(f'{name}.apkg')
