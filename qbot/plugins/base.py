#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class BasePlugin:
    subclasses = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.subclasses.append(cls)
