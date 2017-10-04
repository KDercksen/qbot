#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from . import BasePlugin
import shelve


class KarmaPlugin(BasePlugin):
    def __init__(self, **kwargs):
        self.filepath = './data/karma.db'
        self.regex_mappings = {
            r'(.*)\+\+\s*': self.plus_karma,
            r'(.*)--\s*': self.min_karma,
            r'~karma\s+(.+)': self.karma,
        }

    def plus_karma(self, match):
        key = match.group(1)
        val = self.update(key, 1)
        return f'[karma] {key} now has {val} karma'

    def min_karma(self, match):
        key = match.group(1)
        val = self.update(key, -1)
        return f'[karma] {key} now has {val} karma'

    def update(self, key, val):
        k = key.strip().lower()
        with shelve.open(self.filepath) as db:
            if k not in db:
                db[k] = 0
            db[k] += val
            return db[k]

    def karma(self, match):
        key = match.group(1)
        val = self.update(key, 0)
        return f'[karma] {key} has {val} karma'
