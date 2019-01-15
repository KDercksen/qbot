#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .base import BasePlugin
from glob import glob
from importlib import import_module
from os.path import basename, splitext
import logging

logger = logging.getLogger(__name__)

for m in glob("./qbot/plugins/*_plugin.py"):
    # Get basename and chop off extension
    module = splitext(basename(m))[0]
    logger.debug(f"Importing discovered module: {module}")
    import_module(f"qbot.plugins.{module}")


def collect_plugins(**kwargs):
    patterns = {}
    for c in BasePlugin.subclasses:
        obj = c(**kwargs)
        patterns.update(obj.regex_mappings)
    logger.debug(f"Collected regex patterns: {patterns}")
    return patterns
