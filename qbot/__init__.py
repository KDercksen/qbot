#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .plugins import collect_plugins


__version__ = '0.1'


plugins_map = collect_plugins()
