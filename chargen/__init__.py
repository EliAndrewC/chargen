from __future__ import unicode_literals, division
import json
import traceback
from os.path import join
from functools import wraps

import cherrypy

from sideboard.lib import parse_config, ajax, render_with_templates, DaemonTask

config = parse_config(__file__)

from chargen._version import __version__
from chargen import op
from chargen import constants as c
from chargen.character import Character


@render_with_templates(config['template_dir'])
class Root:
    def index(self):
        conf = config.dict().copy()
        conf.pop('oauth')
        return {
            'config': conf,
            'types': Character.types().keys()
        }

    def tags(self):
        return {}

    @ajax
    def read(self):
        characters = sorted(op.read(), key=lambda c: c['name'])
        return {
            'characters': characters,
            'tags': sorted(set(sum([c['tags'] for c in characters], [])))
        }

    @ajax
    def generate(self, type, **params):
        return Character.types()[type](**params).to_dict()

    @ajax
    def upload(self, name, overview, public, private, tags):
        tags = filter(bool, map(unicode.strip, tags.split(',')))
        character = op.create(name=name, tags=tags, bio=public, game_master_info=private)
        c.USED_NAMES.add(character['name'].split()[-1])
        return {
            'view_url': config['campaign_url'] + '/characters/' + character['slug'],
            'edit_url': config['campaign_url'] + '/characters/' + character['slug'] + '/edit'
        }


def update_used_names():
    c.USED_NAMES.clear()
    c.USED_NAMES.update(op.names())
    c.USED_NAMES.update(c.HOUSE_NAMES)

DaemonTask(update_used_names, interval=600)

cherrypy.tree.mount(Root(), '/chargen')
