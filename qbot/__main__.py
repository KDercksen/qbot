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
    else:
        return 'I don\'t understand :(' if re.match('~.*', line) else None


def main():
    p = ArgumentParser()
    p.add_argument('line')
    p.add_argument('--version', action='version', version=f'qb {__version__}')
    args = p.parse_args()

    response = match_line(args.line)
    if response:
        print(response)


if __name__ == '__main__':
    main()
