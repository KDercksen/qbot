#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from . import plugins_map, __version__
from argparse import ArgumentParser
from configparser import ConfigParser
import logging
import re
import signal
import socket
import sys


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


def irc(servername, host, port, nick, ident, realname, channels):
    def enc(msg):
        return bytes(f'{msg}\r\n', 'UTF-8')

    readbuffer = ''
    commachannels = ','.join(channels)
    s = socket.socket()
    s.connect((host, port))
    s.send(enc(f'NICK {nick}'))
    s.send(enc(f'USER {ident} {host} {servername} :{realname}'))
    s.send(enc(f'JOIN {commachannels}'))
    for c in channels:
        s.send(enc(f'PRIVMSG {c} :Hello!'))

    def graceful_exit(signum, frame):
        s.send(enc(f'QUIT :Bot\'s gotta go! :)'))
        s.close()
        logger.info('Exiting!')
        sys.exit(0)

    # Register SIGINT handler
    signal.signal(signal.SIGINT, graceful_exit)

    while True:
        readbuffer += s.recv(1024).decode('UTF-8')
        temp = readbuffer.split('\n')
        readbuffer = temp.pop()

        for line in temp:
            ls = line.strip()
            logging.debug(f'IRC MESSAGE: {ls}')
            # PING message; respond with PONG <sender>
            pingpong = r'.*?PING\s(.*)'
            # PRIVMSG: group 1 is sender, group 2 is receiver/channel, group 3
            # is message
            privmsg = r':(\w+).*?\sPRIVMSG\s(\#{0,2}\w+)\s:(.*)'
            # response string
            response = ''
            m = re.match(pingpong, ls)
            if m:
                response = f'PONG {m.group(1)}'
                logger.debug(f'Respond to PING: {response}')
                s.send(enc(response))
                continue
            m = re.match(privmsg, ls)
            if m:
                r = match_line(m.group(3))
                if r is not None:
                    response = f'PRIVMSG {m.group(2)} :{r}'
                    logger.debug(f'Respond to command: {response}')
                    s.send(enc(response))
                    continue


def main():
    logger.info('Launched qbot')
    p = ArgumentParser()
    p.add_argument('config', help='Config file (in dry run, '
                                  'this argument should be a sample message')
    p.add_argument('--dry', action='store_true')
    p.add_argument('--version', action='version', version=f'qb {__version__}')
    args = p.parse_args()
    logger.debug(f'Parsed commandline arguments: {args}')

    if not args.dry:
        config = ConfigParser()
        config.read(args.config)
        server = config['server']
        irc(
            server['name'],
            server['host'],
            server.getint('port'),
            server['nick'],
            server['ident'],
            server['realname'],
            server['channels'].split(','),
        )
    else:
        logger.info('Running dry...')
        response = match_line(args.config)
        logger.debug(f'Response for {args.config}: {response}')
        if response:
            print(response)


if __name__ == '__main__':
    main()
