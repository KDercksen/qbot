#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from . import BasePlugin
from urllib.request import urlopen
from urllib.parse import quote
import logging

logger = logging.getLogger(__name__)


class ClooglPlugin(BasePlugin):
    """ClooglPlugin shortens the given url using the cloo.gl shortening service

    Configurable values:
        [cloogl]
        # Should contain the api key
        apikey = a

    Examples:
        user | ~cloogl example.com
        qbot | http://cloo.gl/MzQy

    Matches all messages starting with ~cloogl
    """

    def __init__(self, **kwargs):
        logger.info("Creating cloo.gl plugin instance")
        self.apikey = kwargs["cloogl"]["apikey"]
        self.regex_mappings = {r"~cloogl (.*)": self.cloogl}

    def cloogl(self, user, match):
        url = match.group(1)
        encurl = quote(url)
        apikey = quote(self.apikey)
        logger.debug(f"Shortening: {url}")
        response = urlopen(
            "https://cloo.gl",
            f"type=regular&token={apikey}&url={encurl}".encode("utf-8"),
        )
        short = response.read().decode("utf-8")
        logger.debug(f"response: {short}")
        return short.strip()
