import os
import json
import base64
import re
import traceback
from functools import wraps

import jinja2
import cherrypy

from chargen import config, op, art, constants as c
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
    def upload(self, **kwargs):
        # Handle JSON POST data
        if cherrypy.request.method == 'POST' and cherrypy.request.headers.get('Content-Type', '').startswith('application/json'):
            body = cherrypy.request.body.read()
            data = json.loads(body)
        else:
            data = kwargs

        name = data.get('name', '')
        summary = data.get('summary', '')
        public = data.get('public', '')
        private = data.get('private', '')
        tags = data.get('tags', '')
        image_data = data.get('image_data', '')
        image_embed = ''  # will be set if we upload the image

        slug = name.lower().replace(' ', '-')
        tags_list = list(filter(bool, map(str.strip, tags.split(','))))

        description = public

        # If we have image data, upload it first and prepend the embed
        if image_data:
            try:
                # Decode base64 image data
                image_bytes = base64.b64decode(image_data)

                # Create a safe filename from the character name
                safe_name = re.sub(r'[^a-zA-Z0-9]', '', name.replace(' ', ''))
                filename = f'{safe_name}.png'

                # Upload the image
                file_info = op.upload_image(image_bytes, filename)
                file_id = file_info.get('id')

                if file_id:
                    image_embed = f'[[File:{file_id} | class=media-item-align-none | {filename}]]'

            except Exception as e:
                cherrypy.log(f'Failed to upload image: {e}\n{traceback.format_exc()}')
                raise

        r = op.create_character(name, summary=summary, tags=tags_list, description=description, bio=image_embed, gm_info=private)
        return {
            'view_url': config['campaign_url'] + '/characters/' + slug,
            'edit_url': config['campaign_url'] + '/characters/' + slug + '/edit'
        }

    @ajax
    def art_prompt(self, **character_data):
        """
        Generate a suggested art prompt based on character data.
        The frontend sends the character dict and we return a prompt string.
        """
        # Convert string representations back to appropriate types
        if 'traits' in character_data and isinstance(character_data['traits'], str):
            character_data['traits'] = [t.strip() for t in character_data['traits'].split(',') if t.strip()]
        if 'xp' in character_data:
            character_data['xp'] = int(character_data['xp'])
        return {'prompt': art.generate_prompt(character_data)}

    @ajax
    def generate_art(self, prompt: str):
        """
        Generate an image from the given prompt.
        Returns base64-encoded image data.
        """
        try:
            image_data = art.generate_image_base64(prompt)
            return {'image': image_data, 'error': None}
        except Exception as e:
            return {'image': None, 'error': str(e)}


cherrypy.tree.mount(Root(), '/')
