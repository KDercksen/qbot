#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from . import BasePlugin
import logging

logger = logging.getLogger(__name__)


class TroutPlugin(BasePlugin):
    """TroutPlugin offers one command to slap users with trouts.

    Examples:
        user | ~trout otheruser
        qbot | user slaps otheruser around a bit with a large trout

    Available commands:
        ~trout <string>
            user slaps <string> with trout. <string> can be a user or any other
            single word

        ~help trout
            display help text
    """

    def __init__(self, **kwargs):
        logger.info("Creating trout plugin instance")
        self.regex_mappings = {
            r"~trout\s(\w+).*": self.trout,
            r"~help\s+trout\s*": self.help,
        }

    def trout(self, user, match):
        victim = match.group(1)
        logger.debug(f"Slapping {victim} with trout")
        return f"{user} slaps {victim} around a bit with a large trout"

    def help(self, *args):
        return "[trout] usage: ~trout username"
