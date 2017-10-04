#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from . import BasePlugin
from bs4 import BeautifulSoup
from urllib.request import urlopen
import logging

logger = logging.getLogger(__name__)


class LinksPlugin(BasePlugin):
    def __init__(self, **kwargs):
        logger.info('Creating links plugin instance')
        self.regex_mappings = {
                r'.*?(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|'
                '(?:%[0-9a-fA-F][0-9a-fA-F]))+).*?': self.link_title,
        }

    def link_title(self, match):
        url = match.group(1)
        page = BeautifulSoup(urlopen(url), 'html.parser')
        title = page.title.string
        logger.debug(f'Showing title for URL {url} -- {title}')
        return f'[link] {title} - {url}'
