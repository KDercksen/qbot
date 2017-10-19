#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from . import BasePlugin
from json import loads
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import urlopen
import logging

logger = logging.getLogger(__name__)


class UDPlugin(BasePlugin):
    '''UDPlugin offers a command to look up terms in Urban Dictionary.

    Configurable values:
        [ud]
        # Should contain up to and including question mark for API GET requests
        apiurl = https://api.urbandictionary.com/v0/define?

    Examples:
        user | ~ud jfc
        qbot | [ud] 'JFC': "Jesus Fucking Christ"

        user | ~ud irc
        qbot | [ud] 'IRC': Abbreviation for Internet Relay Chat. A multiplayer
               notepad.

        user | ~ud asdlfkjh
        qbot | [ud] no definition found for 'asdlfkjh'

    Available commands:
        ~ud <term>
            look up definition for term

        ~help ud
            display help text
    '''

    def __init__(self, **kwargs):
        logger.info('Creating ud plugin instance')
        self.url = kwargs['ud']['apiurl']
        self.regex_mappings = {
            r'~ud\s+(.*)': self.get_definition,
            r'~help\s+ud\s*': self.help,
        }

    def get_definition(self, user, match):
        term = match.group(1)
        logger.debug(f'Querying UD for \'{term}\'')
        try:
            params = urlencode({'term': term})
            url = f'{self.url}{params}'
            logger.debug(f'URL: {url}')
            response = loads(urlopen(url).read())
            if response['result_type'] == 'exact':
                topresult = response['list'][0]
                word = topresult['word']
                definition = topresult['definition'].split('\n')[0]
                return f'[ud] \'{word}\': {definition}'
            elif response['result_type'] == 'no_results':
                return f'[ud] no definition found for \'{term}\''
            t = response['result_type']
            return f'[ud] unexpected response type \'{t}\''
        except URLError as e:
            logger.debug(f'Error querying UD: {e.reason}')
            return '[ud] could not connect to UD: API URL wrong or offline?'

    def help(self, *args):
        return '[ud] \'~ud term\' to look up definition of term'
