#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup
import qbot


def parse_requirements(fname):
    with open(fname) as f:
        lines = (line.strip() for line in f)
        return [line for line in lines if line and not line.startswith("#")]


install_reqs = parse_requirements("requirements.txt")


setup(
    name="qbot",
    version=qbot.__version__,
    description="qbot is an easily extendable IRC bot",
    author="Koen Dercksen",
    author_email="mail@koendercksen.com",
    url="https://github.com/KDercksen/qbot",
    install_requires=[ir for ir in install_reqs],
    packages=find_packages(exclude=["tests"]),
    entry_points={"console_scripts": ["qbot=qbot.__main__:main"]},
)
