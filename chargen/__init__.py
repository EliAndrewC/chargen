from __future__ import unicode_literals, division
import json
import traceback
from os.path import join
from functools import wraps

import cherrypy

from sideboard.lib import parse_config, ajax, render_with_templates, DaemonTask

config = parse_config(__file__)

from chargen._version import __version__
from chargen import op, character
from chargen import constants as c


@render_with_templates(config['template_dir'])
class Root:
    def index(self):
        return config

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
    def generate(self, **params):
        return CharType(**params).to_dict()

    @ajax
    def upload(self, name, overview, public, private, tags):
        tags = filter(bool, map(unicode.strip, tags.split(',')))
        character = op.create(name=name, tags=tags, bio=public, game_master_info=private)
        c.USED_NAMES.append(character['name'].split()[-1])
        return {
            'view_url': config['campaign_url'] + '/characters/' + character['slug'],
            'edit_url': config['campaign_url'] + '/characters/' + character['slug'] + '/edit'
        }


def update_used_names():
    c.USED_NAMES[:] = op.names()

DaemonTask(update_used_names, interval=600)

cherrypy.tree.mount(Root(), '/chargen')
