import os
import json
from functools import wraps

import jinja2
import cherrypy

from chargen import config, op, constants as c
from chargen.character import Character

jinja_loader = jinja2.FileSystemLoader(os.path.join(c.HERE, 'templates'))
jinja_env = jinja2.Environment(loader=jinja_loader)


def ajax(func):
    """
    Decorator which takes a function and converts it to one which converts its
    return value to JSON and sets the Content-Type response header.
    """
    @cherrypy.expose
    @wraps(func)
    def wrapped(*args, **kwargs):
        cherrypy.response.headers['Content-Type'] = 'application/json'
        return json.dumps(func(*args, **kwargs)).encode('UTF-8')
    return wrapped


class Root:
    @cherrypy.expose
    def index(self):
        return jinja_env.get_template('index.html').render({
            'config': config.dict(),
            'types': list(Character.types().keys())
        }).encode('UTF-8')

    @ajax
    def generate(self, type: str, **params):
        """
        This is invoked when the frontend wants to make a character; we return a
        randomly generated character of the given type (e.g. "samurai").
        """
        return Character.types()[type](**params).to_dict()

    @ajax
    def upload(self, name: str, summary: str, public: str, private: str, tags: list[str]):
        slug = name.lower().replace(' ', '-')
        tags = filter(bool, map(str.strip, tags.split(',')))
        r = op.create_character(name, summary=summary, tags=tags, description=public, gm_info=private)
        return {
            'view_url': config['campaign_url'] + '/characters/' + slug,
            'edit_url': config['campaign_url'] + '/characters/' + slug + '/edit'
        }


cherrypy.tree.mount(Root(), '/')
