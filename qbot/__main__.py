#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from . import plugins_map, __version__
from argparse import ArgumentParser
import logging
import re


logging.basicConfig(
    format='%(levelname)s:%(asctime)s:%(name)s:%(message)s',
    filename='qbot.log',
    level=logging.DEBUG,
)

logger = logging.getLogger(__name__)


def match_line(line):
    logger.debug(f'Matching line: {line}')
    for pattern, func in plugins_map.items():
        m = re.match(pattern, line)
        if m:
            return func(m)
    else:
        return 'I don\'t understand :(' if re.match('~.*', line) else None


def main():
    logger.info('Launched qbot')
    p = ArgumentParser()
    p.add_argument('line')
    p.add_argument('--version', action='version', version=f'qb {__version__}')
    args = p.parse_args()
    logger.debug(f'Parsed commandline arguments: {args}')

    response = match_line(args.line)
    logger.debug(f'Response for {args.line}: {response}')
    if response:
        print(response)


if __name__ == '__main__':
    main()
