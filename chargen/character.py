from __future__ import unicode_literals
from os.path import join
from copy import deepcopy
from random import random, randrange, normalvariate, choice

from chargen import constants as c


def rounded(x, minval=1, maxval=15):
    return min(maxval, max(minval, round(x * 2) / 2))


def unused_name(gender=None):
    name = None
    while not name or name in c.USED_NAMES:
        name = choice(c.NAMES[gender or choice(['male','female'])])
    return name


def weighted_choice(d):
    assert sum(d.values()) <= 100
    roll = randrange(100)
    total = 0
    for choice, percent in d.items():
        total += percent
        if roll < total:
            return choice


class Character(object):
    def __init__(self, base_rank, gender=None, clan=None, family=None, house=None, lineage=None, school=None):
        base_rank = int(base_rank)
        self.rank = rounded(normalvariate(base_rank, 0.3), minval=base_rank - 1, maxval=base_rank + 1)
        self.recognition = rounded(normalvariate(self.rank, 1))

        self.clan = clan or weighted_choice(config['clans'])
        self.family = clan or weighted_choice(config['clan'].get(self.clan))
        self.house = house or weighted_choice(config['family'].get(self.family))
        self.lineage = lineage or weighted_choice(config['house'].get(self.house))
        self.school = school or weighted_choice(config['clan'].get(self.clan, {}).get('schools', config['schools']['default']))

        self.gender = gender or choice(['male', 'female'])
        self.personal_name = unused_name(self.gender)

        self.xp = self.gen_xp()
        self.gen_honor()
        self.gen_traits()
        self.id = str(randrange(1e9))

    def gen_xp(self):
        if self.xp:
            return self.xp

        base = 0
        for rank, rank_base in config['rank_xp_bases'].items():
            if self.rank >= int(rank):
                base = rank_base

        while random() < 0.10:
            base += 50
        return base + 5 * randrange(10)

    def gen_honor(self, base=2.5):
        if random() < 0.50 + self.rank * 0.03:
            self.honor = rounded(base + abs(normalvariate(0, 1)), maxval=6)
        else:
            self.honor = rounded(base - abs(normalvariate(0, 0.5)), minval=1)

    def gen_traits(self):
        self.traits = []
        for trait, chance in dict(c.TRAITS, **c.GENDER_TRAITS[self.gender]).items():
            if '/' in trait:
                for t, c in zip(trait.split('/'), chance):
                    if random() < c:
                        self.traits.append(t.strip())
                        break
            else:
                if random() < chance:
                    self.traits.append(trait)
        self.traits.sort()

    def to_dict(self):
        data = deepcopy(self.__dict__)
        data['public'] = self.render('public_info.txt', data)
        data['private'] = self.render('private_info.txt', data)
        return data

    def __repr__(self):
        return repr(self.to_dict())

    def render(self, fname, data):
        stats = deepcopy(data) or self.to_dict()
        for stat, value in stats.items():
            if isinstance(value, list):
                stats[stat] = '\n'.join(value)

        with open(join(config['template_dir'], fname)) as f:
            return f.read().format(**stats).strip()

