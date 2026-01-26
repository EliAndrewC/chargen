import os

from chargen import config, __here__ as HERE

__all__ = ['HERE', 'NAMES', 'USED_NAMES', 'XP_DIST', 'TRAITS', 'GENDER_TRAITS', 'MINISTRIES']


NAMES = {}
"""
This is how we store gender-organized names and their meanings, e.g.
    {
        'male': {
            'Akio': 'This name represents "bright man" and is often chosen by those who are naturally charismatic or who are expected to become influential leaders.',
        ...
        },
        'female': {...}
    }
"""
for _gender in ['male', 'female']:
    with open(os.path.join(HERE, f'{_gender}_names.txt')) as f:
        name_lines = [line.strip() for line in f if line.strip()]
        NAMES[_gender] = {
            line.split()[0]: line.split(' - ', 1)[1] if line.split()[1] == '-' else line
            for line in name_lines
        }

USED_NAMES = set()
"""
This is updated with the personal names (e.g. 'Gohei' instead of 'Matsu Gohei')
of all of the characters already in Obsidian Portal.
"""

HOUSE_NAMES = set()
"""
Different campaigns involve different houses, and this pulls those from 
"""
for _family in config['family'].values():
    HOUSE_NAMES.update(name.title() for name in _family.keys())

XP_DIST = [.80, .65, .50, .35, .20, .18, .16, .14, .12, .10]
"""
See the gen_xp() function in character.py for an explanation of the experience
distribution which this represents.
"""

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
    'deferential / outspoken': (0.10, 0.05),

    'interrupting': 0.10,
    'tattooed': 0.05,
    'collector': 0.05,
    'garishly dressed': 0.05,
    'pensive': 0.05,
    'scarred': 0.01,
    'hairy arms': 0.01,
}
"""
When randomly generating traits, we iterate through this list; the keys are the
traits and the values are the percentage of NPCs with that trait.  Some of these
are advantages/disadvantages and others are general descriptions.

Some traits are mutually exclusive with one anopther, so in those cases we
represent it as e.g.

    'Vain / Unkempt': (0.10, 0.05)

which means that there's a 10% chance of Vain and a 5% chance of Unkempt.  This
is implemented via the gen_traits() method in character.py
"""

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
"""
Some traits are gender-specific, e.g. 'mustachioed' or 'pregnant'.  This uses
the same format as TRAITS above, indexed by gender.
"""

CLAN_COLORS = {
    'Crab': 'dark blue and light gray',
    'Crane': 'light blue and white / silver',
    'Dragon': 'gold and dark green',
    'Lion': 'yellow and brown',
    'Phoenix': 'red and orange',
    'Scorpion': 'black and dark red',
    'Unicorn': 'purple and white with gold trim',
    'Sparrow': 'dun brown and black',
    'Fox': 'green and silver',
    'Wasp': 'black and gold',
    'Dragonfly': 'blue, brown, and gold',
    'Hare': 'red and white',
}
"""
This is not yet used, but art.py will eventually make use of this when making
art prompts for NPCs.
"""

MINISTRIES = [
    'Ministry of Rites',
    'Ministry of Retainers',
    'Ministry of Revenue',
    'Ministry of War',
    'Ministry of Works',
    'Ministry of Justice'
]
"""
The six ministries of the Rokugan imperial bureaucracy. Each ministry has
specific responsibilities and is led by a Minister and Deputy Minister at
the imperial level, with Provincial and Deputy Provincial Ministers in
the provinces.
"""
