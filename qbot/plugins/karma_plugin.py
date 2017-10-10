#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from . import BasePlugin
import logging
import shelve

logger = logging.getLogger(__name__)


class KarmaPlugin(BasePlugin):
    '''KarmaPlugin offers a set of commands to keep track of karma for certain
    words/sentences.

    Configurable values:
        [karma]
        filepath = /path/to/karma.db

    Examples:
        user | qbot++
        qbot | [karma] qbot now has 1 karma

        user | qbot--
        qbot | [karma] qbot now has 0 karma

        user | ~karma qbot
        qbot | [karma] qbot has 0 karma

    Available commands:
        <string>++
            add 1 karma to string

        <string>--
            take 1 karma from string

        ~karma <string>
            check current karma for string

        ~help karma
            display help text
    '''

    def __init__(self, **kwargs):
        logger.info('Creating karma plugin instance')
        self.filepath = kwargs['karma']['filepath']
        self.regex_mappings = {
            r'(.*)\+\+\s*': self.plus_karma,
            r'(.*)--\s*': self.min_karma,
            r'~karma\s+(.+)': self.karma,
            r'~help\s+karma\s*': self.help,
        }

    def plus_karma(self, user, match):
        key = match.group(1)
        logger.debug(f'Adding karma to {key}')
        val = self.update(key, 1)
        return f'[karma] {key} now has {val} karma'

    def min_karma(self, user, match):
        key = match.group(1)
        logger.debug(f'Taking karma from {key}')
        val = self.update(key, -1)
        return f'[karma] {key} now has {val} karma'

    def update(self, key, val):
        k = key.strip().lower()
        with shelve.open(self.filepath) as db:
            if k not in db:
                db[k] = 0
            db[k] += val
            return db[k]

    def karma(self, user, match):
        key = match.group(1)
        logger.debug(f'Showing karma for {key}')
        val = self.update(key, 0)
        return f'[karma] {key} has {val} karma'

    def help(self, *args):
        return '[karma] \'something++\' or \'something--\' to add/subtract ' \
               'karma; use \'~karma something\' to check current karma'
