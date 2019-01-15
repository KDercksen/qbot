#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from . import BasePlugin
from json import loads
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import urlopen
import logging

logger = logging.getLogger(__name__)


class WeatherPlugin(BasePlugin):
    """WeatherPlugin offers a single command for querying current weather
    conditions for a certain city.

    Configurable values:
        [weather]
        apiurl = https://api.openweathermap.org/data/2.5/weather?
        apikey = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        # Possible values: metric, imperial, or leave out for Fahrenheit
        units = metric

    Examples:
        user | ~weather London
        qbot | [weather] London: broken clouds, temp: 20, humidity: 80%,
               cloudiness: 50%, rain for last 3h: 13

    Available commands:
        ~weather <city>[,<countrycode>]
            look up weather for city name, with optional country code (UK, NL,
            etc).

        ~help weather
            display help text
    """

    def __init__(self, **kwargs):
        self.url = kwargs["weather"]["apiurl"]
        self.key = kwargs["weather"]["apikey"]
        self.units = kwargs["weather"].get("units", None)
        self.regex_mappings = {
            r"~weather\s+(.*)": self.get_weather,
            r"~help\s+weather\s*": self.help,
        }
        self.temp_units = {"metric": "C", "imperial": "K", None: "F"}

    def get_weather(self, user, match):
        query = match.group(1)
        logger.debug(f"Querying weather API for '{query}'")
        params = {"q": query, "appid": self.key}
        if self.units:
            params["units"] = self.units
        encparams = urlencode(params)
        url = f"{self.url}{encparams}"
        logger.debug(f"URL: {url}")
        try:
            response = loads(urlopen(url).read())
            city = response["name"]
            weather = response["weather"][0]["description"]
            temp = response["main"]["temp"]
            humidity = response["main"]["humidity"]
            clouds = response["clouds"]["all"]
            try:
                rain = response["rain"]["3h"]
            except KeyError:
                rain = 0
            return (
                f"[weather] {city}: {weather}, temp: {temp}"
                f"{self.temp_units[self.units]}, humidity: {humidity}%, "
                f"cloudiness: {clouds}%, rain for last 3h: {rain}mm"
            )
        except URLError as e:
            logger.debug(f"Error querying weather API: {e.reason}")
            return f"[weather] could not connect to API"

    def help(self, *args):
        return f"[weather] '~weather city[,countrycode]' to look up weather"
