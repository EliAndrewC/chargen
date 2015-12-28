from __future__ import unicode_literals
import json

import requests
from requests_oauthlib import OAuth1

from chargen import config
from chargen import constants as c

oauth = OAuth1(config['client_key'], config['client_secret'],
               config['oauth_account_token'], config['oauth_account_secret'],
               signature_type='auth_header')


def req(method, url, data={}):
    resp = getattr(requests, method)(url, auth=oauth, data=json.dumps(data), headers={'Content-Type': 'application/json'})
    try:
        data = resp.json()
    except:
        raise ValueError('Could not decode json: {}'.format(resp.content))
    else:
        if 'errors' in data:
            raise AssertionError(str(data))
        else:
            return data


def create(**params):
    character = c.CHARACTER_DEFAULTS.copy()
    character.update(params)
    return req('post', config['character_url'], {'character': character})


def read():
    return req('get', config['character_url'])


def names():
    return {character['name'].split()[-1] for character in read()}
