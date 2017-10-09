#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from . import BasePlugin
from random import choice
import logging
import shelve

logger = logging.getLogger(__name__)


class QuotePlugin(BasePlugin):
    '''QuotePlugin offers a set of commands to add/search/remove quotes
    associated with specific topics.

    Examples:
        user | ~qadd topic=What do you think about QuotePlugin?
        qbot | [quote] quote added to 'topic'

        user | ~qshow topic
        qbot | [quote] topic: What do you think about QuotePlugin?

        user | ~qsearch topic=quoteplugin
        qbot | [quote] topic (quoteplugin): 'What do you think about
               QuotePlugin?' [1 result]

        user | ~qrm topic=What do you think about QuotePlugin?
        qbot | [quote] quote removed from 'topic'

    Available commands:
        ~qadd <key>=<quote>
            adds a quote under a certain key (key is case-insensitive)

        ~qshow <key>
            show a random quote out of all quotes associated with key

        ~qsearch <key>=<query>
            find quotes containing query (case-insensitive) under key; if
            multiple are found, show a random pick

        ~qrm <key>=<quote>
            remove this quote from keys quotes; this only works when the quote
            is an exact match
    '''

    def __init__(self, **kwargs):
        logger.info('Creating quote plugin instance')
        self.filepath = kwargs['quote']['filepath']
        keyisval = r'((?:\w+\s*?)+)\s*=\s*(.*)'
        self.regex_mappings = {
            fr'~qadd\s+{keyisval}': self.quote_add,
            fr'~qsearch\s+{keyisval}': self.quote_search,
            fr'~qrm\s+{keyisval}': self.quote_rm,
            fr'~qshow\s+(.*)': self.quote_show,
            r'~help\s+quote\s*': self.help,
        }

    def quote_add(self, user, match):
        key = match.group(1).lower()
        quote = match.group(2).strip()
        logger.debug(f'Adding ({key}, {quote})')
        with shelve.open(self.filepath) as db:
            if key not in db:
                db[key] = []
            # This is needed because of shelves being a little fickle
            temp = db[key]
            temp.append(quote)
            db[key] = temp
            num = len(db[key])
            return f'[quote] quote added to \'{key}\' [{num} total]'

    def quote_search(self, user, match):
        key = match.group(1).lower()
        query = match.group(2).strip().lower()
        logger.debug(f'Searching for {query} in {key} quotes')
        with shelve.open(self.filepath) as db:
            if key not in db:
                logger.debug(f'No quotes found for {key}')
                return f'[quote] no quotes found for \'{key}\''
            results = [q for q in db[key] if query in q.lower()]
            num = len(results)
            s = 's' if num > 1 else ''
            quote = choice(results)
            logger.debug(f'Returning {quote} from {num} result{s}')
            return f'[quote] {key} ({query}): \'{quote}\' [{num} result{s}]'

    def quote_rm(self, user, match):
        key = match.group(1).lower()
        quote = match.group(2).strip()
        logger.debug(f'Attempting to remove \'{quote}\' from {key} quotes')
        with shelve.open(self.filepath) as db:
            if key not in db:
                logger.debug(f'No quotes found for {key}')
                return f'[quote] no quotes found for \'{key}\''
            if quote in db[key]:
                db[key].remove(quote)
                logger.debug(f'Removed \'{quote}\' from {key}')
                return f'[quote] quote removed from \'{key}\''
            logger.debug('Quote could not be found in \'{key}\' quotes')
            return f'[quote] no such quote found for \'{key}\''

    def quote_show(self, user, match):
        key = match.group(1).strip().lower()
        with shelve.open(self.filepath) as db:
            if key not in db:
                return f'[quote] no quotes found for \'{key}\''
            quote = choice(db[key])
            num = len(db[key])
            s = 's' if num > 1 else ''
            return f'[quote] {key}: {quote} [{num} result{s}]'

    def help(self, *args):
        return '[quote] available commands: ~qadd <key>=<val>, ' \
               '~qrm <key>=<val>, ~qshow <key>, ~qsearch <key>=<val> | ' \
               'check plugin source code for more info (~help)'
