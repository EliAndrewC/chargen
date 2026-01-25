"""
Obsidian Portal (op) has an OAuth 1.0 API.  This file uses that API to upload
characters, as well as download existing data from the campaign, documented at
    https://help.obsidianportal.com/article/105-api-authentication-oauth
"""
from time import sleep
from threading import Thread

import cherrypy

from chargen import config
from chargen import constants as c


def create_character(name, *, summary, description, gm_info) -> dict:
    """
    Given a set of character information, create a character in Obsidian Portal
    and then return the dict of character info which the OP API returns.
    """
    # TODO: this needs to be written


def existing_names() -> list[str]:
    """
    This reaches out to Obsidian Portal using their API and returns a list of
    all character names for the campaign.
    """
    # TODO: this needs to be written


def update_used_names():
    """
    We keep track of what names already exist in our campaign to avoid using the
    same name multiple times.  Every time we create a character, we add its name
    to our global name set, but here we also periodically download everything in
    the background to update the list, in case we missed anything (e.g. if a new
    character was added through the Obsidian Portal UI instead of here).
    """
    while True:
        for name in existing_names():
            c.EXISTING_NAMES.add(name.split()[-1])  # we only track the personal name (e.g. "Gohei" instead of "Matsu Gohei")
        sleep(3600)


existing_name_updater = Thread(target=update_used_names, daemon=True)
cherrypy.engine.subscribe('start', existing_name_updater.start)
