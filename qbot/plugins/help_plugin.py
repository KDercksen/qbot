#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from . import BasePlugin
import logging

logger = logging.getLogger(__name__)


class HelpPlugin(BasePlugin):
    '''HelpPlugin offers a simple link to QBots documentation.

    Example:
        user | ~help
        qbot | [help] For usage help, see http://github.com/KDercksen/qbot

    Available commands:
        ~help
            show link to usage instructions
    '''

    def __init__(self, **kwargs):
        logger.info('Creating help plugin instance')
        self.regex_mappings = {
            r'~help.*': self.help_link,
        }

    def help_link(self, *args):
        logger.debug('Displaying help link')
        return f'[help] For usage help, see http://github.com/KDercksen/qbot'
