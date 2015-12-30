from __future__ import unicode_literals
import os
import json

from chargen import config

__all__ = ['NAMES', 'USED_NAMES', 'CHARACTER_DEFAULTS', 'XP_DIST', 'TRAITS', 'GENDER_TRAITS']

with open(os.path.join(config['root'], 'names.json')) as f:
    NAMES = json.load(f)

USED_NAMES = []

XP_DIST = [.80, .65, .50, .35, .20, .18, .16, .14, .12, .10]

CHARACTER_DEFAULTS = {
    'bio': '',
    'tags': [],
    'tagline': '',
    'description': '',
    'game_master_info': '',
    'is_game_master_only': False,
    'is_player_character': False,
    'author_id': config['author_id']
}

TRAITS = {
    'Poor / Wealthy': (0.20, 0.20),
    'Vain / Unkempt': (0.10, 0.05),
    'Virtue / Unconventional': (0.10, 0.05),

    'Short Temper': 0.10,
    'Long Temper': 0.10,
    'Contrary': 0.15,
    'Good Reputation': 0.10,

    'Bad Reputation': 0.05,
    'Imperial Favor': 0.05,
    'Kind Eye': 0.10,
    'Jealousy': 0.05,
    'Permanent Wound': 0.10,

    'Dark Secret': 0.01,
    'Driven': 0.02,
    'Emotional': 0.05,
    'Humble': 0.05,
    'Transparent': 0.05,
    'Thoughtless': 0.05,

    'thin / fat': (0.05, 0.05),
    'short / tall': (0.05, 0.05),
    'big nose / big ears': (0.01, 0.01),
    'boisterous / soft-spoken': (0.05, 0.05),
    'missing tooth / missing finger': (0.01, 0.01),
    'dour / scowling / furrowed / frowny / squinty': (0.01, 0.01, 0.01, 0.01, 0.01),
    'jolly / happy / lighthearted / mirthful / upbeat': (0.01, 0.01, 0.01, 0.01, 0.01),
    'quick to speak / pauses before speaking': (0.05, 0.05),
    'deferential / precocious': (0.10, 0.05),

    'interrupting': 0.10,
    'tattooed': 0.05,
    'collector': 0.05,
    'garishly dressed': 0.05,
    'pensive': 0.05,
    'scarred': 0.01,
    'hairy arms': 0.01,
}
GENDER_TRAITS = {
    'male': {
        'balding': 0.20,
        'bearded / long beard / bushy beard / mustachioed': (0.10, 0.02, 0.02, 0.05),
    },
    'female': {
        'pregnant': 0.15,
        'jewelried': 0.10,
        'fine makeup / inexpert makeup': (0.10, 0.05)
    }
}
