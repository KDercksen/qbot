#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from . import plugins_map, __version__
from argparse import ArgumentParser
import re


def match_line(line):
    for pattern, func in plugins_map.items():
        m = re.match(pattern, line)
        if m:
            return func(m)
    return 'I don\'t know what you mean :('


def main():
    p = ArgumentParser()
    p.add_argument('line')
    p.add_argument('--version', action='version', version=f'qb {__version__}')
    args = p.parse_args()
    print(match_line(args.line))


if __name__ == '__main__':
    main()
