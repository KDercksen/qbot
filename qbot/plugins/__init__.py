#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .base import BasePlugin
from glob import glob
from importlib import import_module
from os.path import basename, splitext

for m in glob('./qbot/plugins/*_plugin.py'):
    # Get basename and chop off extension
    module = splitext(basename(m))[0]
    import_module(f'qbot.plugins.{module}')


def collect_plugins():
    patterns = {}
    for c in BasePlugin.subclasses:
        obj = c()
        patterns.update(obj.regex_mappings)
    return patterns


__all__ = [c.__name__ for c in BasePlugin.subclasses]
