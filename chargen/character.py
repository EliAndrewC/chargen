from __future__ import unicode_literals
from os.path import join
from copy import deepcopy
from random import random, randrange, normalvariate, choice

from chargen import config
from chargen import constants as c


def rounded(x, minval=1, maxval=15):
    return min(maxval, max(minval, round(x * 2) / 2))


def unused_name(gender=None):
    name = None
    while not name or name in c.USED_NAMES:
        name = choice(c.NAMES[gender or choice(['male','female'])])
    return name


def weighted_choice(d):
    if d:
        roll = randrange(sum(d.values()))
        total = 0
        for choice, percent in d.items():
            total += percent
            if roll < total:
                return choice
    else:
        return ''


class Character(object):
    def __init__(self):
        self.gender = choice(['male', 'female'])
        self.personal_name = unused_name(self.gender)

        self.xp = self.gen_xp()
        self.honor = self.gen_honor()
        self.traits = self.gen_traits()
        self.tags = self.gen_tags()
        self.id = str(randrange(1e9))

    @classmethod
    def types(cls):
        types = {}
        for subclass in cls.__subclasses__():
            types[subclass.__name__] = subclass
            types.update(subclass.types())
        return types

    def gen_xp(self):
        base = 0
        for rank, rank_base in config['rank_xp_bases'].items():
            if self.rank >= int(rank):
                base = rank_base

        while random() < 0.10:
            base += 50
        return base + 5 * randrange(10)

    def gen_honor(self, base=2.0):
        if random() < 0.50 + self.rank * 0.03:
            return rounded(base + abs(normalvariate(0, 1.0)), maxval=5)
        else:
            return rounded(base - abs(normalvariate(0, 0.5)), minval=1)

    def gen_traits(self):
        traits = []
        for trait, chance in dict(c.TRAITS, **c.GENDER_TRAITS[self.gender]).items():
            if '/' in trait:
                for subtrait, subchance in zip(trait.split('/'), chance):
                    if random() < subchance:
                        traits.append(subtrait.strip())
                        break
            else:
                if random() < chance:
                    traits.append(trait)
        return sorted(traits)

    def gen_tags(self):
        return filter(None, [
            self.clan and (self.clan_display + (' Clan' if self.clan != 'imperial' else '')),
            self.family and (self.family_display + ' Family'),
            self.house and (self.house_display + ' House'),
            self.lineage and (self.lineage_display + ' Lineage')
        ])

    def render(self, fname):
        with open(join(config['template_dir'], fname)) as f:
            return f.read().format(character=self).strip()

    def to_dict(self):
        return dict(self.__dict__, **{
            'public': self.render('public_info.txt'),
            'private': self.render('private_info.txt')
        })

    def __getattr__(self, name):
        if name.endswith('_display'):
            return getattr(self, name.rsplit('_', 1)[0]).replace('_', ' ').title()
        elif name.endswith('_string'):
            return '\n'.join(getattr(self, name.rsplit('_', 1)[0]))
        else:
            raise AttributeError('no such attribute: ' + name)

    def __repr__(self):
        return repr(self.to_dict())


class Samurai(Character):
    def __init__(self, base_rank, clan=None, family=None, house=None, lineage=None, school=None):
        self.base_rank = int(base_rank)
        self.rank = rounded(normalvariate(self.base_rank, 0.3), minval=self.base_rank - 1, maxval=self.base_rank + 1)
        self.recognition = rounded(normalvariate(self.rank, 1))

        self.clan = clan or weighted_choice(config['clans'])
        self.family = family or weighted_choice(config['clan'].get(self.clan, {}))
        self.house = house or weighted_choice(config['family'].get(self.family, {}))
        self.lineage = lineage or weighted_choice(config['house'].get(self.house, {}))
        self.school = school or weighted_choice(config['schools'].get(self.clan, config['schools']['default']))

        Character.__init__(self)

        self.full_name = ' '.join(filter(None, [
            self.family_display,
            'no {}'.format(self.house_display) if self.house else '',
            self.personal_name
        ]))


class Peasant(Character):
    def __init__(self, base_rank=0, **ignored):
        self.rank = int(base_rank)
        Character.__init__(self)
        self.recognition = rounded(normalvariate(self.rank + 2, 1))
        self.full_name = self.personal_name


class Legionnaire(Samurai):
    def gen_tags(self):
        return Character.gen_tags(self) + filter(None, [
            config['company'].get(self.house, choice(list(set(config['company'].values())))),
            config['ranks'].get(str(self.base_rank))
        ])

