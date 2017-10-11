#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from . import BasePlugin
from bs4 import BeautifulSoup
from urllib.request import urlopen
import logging

logger = logging.getLogger(__name__)


class LinkPlugin(BasePlugin):
    '''LinkPlugin displays the titles of the webpages linked in the IRC
    channel.

    Examples:
        user | https://google.com
        qbot | [link] Google - https://google.com

        user | check out this site: https://en.wikipedia.org/wiki/HTML
        qbot | [link] HTML - Wikipedia - https://en.wikipedia.org/wiki/HTML

    Matches all messages containing an URL starting with http(s). Currently
    URLs without protocol (i.e. 'google.com' or 'www.google.com') are not
    supported.
    '''

    def __init__(self, **kwargs):
        logger.info('Creating links plugin instance')
        self.regex_mappings = {
                r'.*?(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|'
                '(?:%[0-9a-fA-F][0-9a-fA-F]))+).*?': self.link_title,
        }

    def link_title(self, user, match):
        url = match.group(1)
        response = urlopen(url)
        if 'text/html' in response.getheader('Content-Type'):
            page = BeautifulSoup(response, 'html.parser')
            title = page.title.string
            logger.debug(f'Showing title for URL {url} -- {title}')
            return f'[link] {title} - {url}'
        else:
            return f'[link] {url}'
