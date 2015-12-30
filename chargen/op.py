from __future__ import unicode_literals, print_function
import json

from rauth import OAuth1Session, OAuth1Service

from sideboard.lib import entry_point

from chargen import config
from chargen import constants as c

session = OAuth1Session(
    access_token=config['oauth']['token'],
    access_token_secret=config['oauth']['secret'],
    consumer_key=config['oauth']['app_token'],
    consumer_secret=config['oauth']['app_secret']
)


def req(method, url, data={}):
    resp = getattr(session, method)(url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
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


@entry_point
def generate_oauth_token():
    service = OAuth1Service(
        name='op',
        consumer_key=config['oauth']['app_token'],
        consumer_secret=config['oauth']['app_secret'],
        **{k: v for k, v in config['oauth'].items() if k in ['request_token_url', 'access_token_url', 'authorize_url']}
    )
    request_token, request_secret = service.get_request_token()
    print('To generate an oauth token, visit the following URL', service.get_authorize_url(request_token), sep='\n')
    pin = raw_input('and paste the verification code here: ').strip()

    session = service.get_auth_session(request_token, request_secret, method='POST', data={'oauth_verifier': pin})
    try:
        session.get(config['api_url_base'] + '/users/me.json').json()
    except:
        print('That verification code failed to work.')
    else:
        print('\nThe following oauth token and secret were generated:')
        print('token =', session.access_token)
        print('secret = ', session.access_token_secret)
