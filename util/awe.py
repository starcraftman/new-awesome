"""
Control the web project from command line.

Relies on internal python apis.
"""
from __future__ import absolute_import, print_function
import argparse
from argparse import RawDescriptionHelpFormatter as RawDescriptionHelp
import os
import sys

import conf
import util
import util.db_control as dbc
# import util.awe_web as webc
# import web


def parse_clean(args):
    """
    Parse: awe clean
    """
    print('Deleting files under root matching: .cache | __pycache__ | *.pyc')
    fnames = util.glob_rec(util.ROOT, r'__pycache__|\.cache|.*\.pyc',
                           ['.git', '.tox', '.vagrant', '.venv'])
    for fname in fnames:
        util.delete_it(fname)

    if args.all:
        for fname in ['.tox', '.venv', 'db/rethink', 'node_modules']:
            path = os.path.join(util.ROOT, fname)
            print('Deleting:', path)
            util.delete_it(path)


def parse_conf(args):
    """
    Parse: awe conf
    """
    conf.update_env(args.env)


def parse_db_start(_):
    """
    Parse: awe db start
    """
    if not dbc.pid():
        print('Starting the database')
        dbc.start()
    else:
        dbc.status()


def parse_db_stop(_):
    """
    Parse: awe db stop
    """
    if dbc.pid():
        print('Please be patient, stopping the database')
        dbc.stop()
    else:
        dbc.status()


def parse_db_restart(_):
    """
    Parse: awe db restart
    """
    print('Please be patient, restarting the database')
    dbc.restart()


def parse_db_status(_):
    """
    Parse: awe db status
    """
    dbc.status()


def parse_db_log(args):
    """
    Parse: awe db log
    """
    print('Last {0} lines of {1}'.format(args.lines, conf.get('db_log')))
    print('-' * 60)
    print(''.join(dbc.log(int(args.lines))))


def parse_db_init(_):
    """
    Parse awe db init
    """
    dbc.init()


def parse_server(args):
    """
    Parse: awe server
    """
    print('Not currently bound')
    print(str(args))


def create_args_parser():
    """
    Create the program argument parser.

    Returns:
        An argparse parser object.
    """
    prog_name = os.path.basename(__file__)[:-3]
    mesg = """
    Unified interface to control this web project.

    See subcommands for specific tasks.
    """
    mesg = mesg[0:-5]
    parser = argparse.ArgumentParser(prog=prog_name, description=mesg,
                                     formatter_class=RawDescriptionHelp)
    subs = parser.add_subparsers()

    sub = subs.add_parser('clean', description='Clean up project')
    sub.set_defaults(func=parse_clean)
    sub.add_argument('-a', '--all', action='store_true',
                     help='remove all possible traces')

    sub = subs.add_parser('conf', description='change global configuration')
    sub.set_defaults(func=parse_conf)
    sub.add_argument('env', choices=['dev', 'test'],
                     help='the type of configuration to deploy')

    sub = subs.add_parser('db', description='Manage the database instance.')
    subs2 = sub.add_subparsers()
    sub = subs2.add_parser('log', description='read back log')
    sub.set_defaults(func=parse_db_log)
    sub.add_argument('lines', nargs='?', default=10, help='show last n lines')
    sub = subs2.add_parser('pid', description='database process id')
    sub.set_defaults(func=lambda _: print(dbc.pid()))
    sub = subs2.add_parser('restart', description='restart the db')
    sub.set_defaults(func=parse_db_restart)
    sub = subs2.add_parser('start', description='start the db')
    sub.set_defaults(func=parse_db_start)
    sub = subs2.add_parser('status', description='status of the db')
    sub.set_defaults(func=parse_db_status)
    sub = subs2.add_parser('stop', description='stop the db')
    sub.set_defaults(func=parse_db_stop)
    sub = subs2.add_parser('init', description='initialize the db')
    sub.set_defaults(func=parse_db_init)

    sub = subs.add_parser('server', description='Manage the server')
    subs2 = sub.add_subparsers()
    sub = subs2.add_parser('restart', description='restart the db')
    sub.set_defaults(func=parse_server)
    sub = subs2.add_parser('start', description='start the db')
    sub.set_defaults(func=parse_server)
    sub = subs2.add_parser('status', description='status of the db')
    sub.set_defaults(func=parse_server)
    sub = subs2.add_parser('stop', description='stop the db')
    sub.set_defaults(func=parse_server)

    return parser


def main(argv=None):
    """
    Main entry point.
    """

    if argv is None:
        argv = sys.argv

    parser = create_args_parser()
    if len(argv) == 1:
        print('No arguments. What should I do?')
        parser.print_usage()
        sys.exit(1)

    args = parser.parse_args(argv[1:])
    args.func(args)


if __name__ == "__main__":
    main()
