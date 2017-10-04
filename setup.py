#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pip.req import parse_requirements
from setuptools import find_packages, setup
import qbot


install_reqs = parse_requirements('requirements.txt', session=False)


setup(
    name='qbot',
    version=qbot.__version__,
    description='qbot is an easily extendable IRC bot',
    author='Koen Dercksen',
    author_email='mail@koendercksen.com',
    url='https://github.com/KDercksen/qbot',
    install_requires=[str(ir.req) for ir in install_reqs],
    packages=find_packages(exclude=['tests']),
    entry_points={
        'console_scripts': ['qbot=qbot.__main__:main'],
    },
)
