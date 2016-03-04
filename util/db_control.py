"""
All logic related to managing the database instance.
"""
from __future__ import absolute_import, print_function
import os
import time

import rethinkdb as r

import conf
import util
import db.common

MAX_TIME = 5


class DBTimeout(Exception):
    """
    Interacting with the db process timed out.
    """
    pass


def pid():
    """
    Returns the pid of the rethinkdb server.
    """
    db_pid = None
    if os.path.exists(conf.get('db_pid')):
        with open(conf.get('db_pid')) as fin:
            db_pid = int(fin.readline())

    return db_pid


def alive():
    """
    The database is alive.
    """
    return pid() and util.pid_alive(pid())


def status():
    """
    Simply print the status of the database.
    """
    if alive():
        print('PID:', str(pid()), 'Root:', conf.get('db_root'))
        print('-' * 60)
        print(''.join(log(5)))
    elif os.path.exists(conf.get('db_pid')):
        print('database improperly shut down')
    else:
        print('database not running')


def start():
    """
    Start the database.
    """
    if pid():
        return

    if not os.path.exists(os.path.join(conf.get('db_root'), 'metadata')):
        util.command('rethinkdb create -d ' + conf.get('db_root'))
    util.command('rethinkdb serve --config-file ' + conf.DB_FILE)

    start_time = time.time()
    while True:
        try:
            db.common.connect()
            break
        except r.errors.ReqlDriverError:
            time.sleep(1)
            if (time.time() - start_time) > MAX_TIME:
                raise DBTimeout()


def stop():
    """
    Stop the database.
    """
    db_pid = pid()
    if db_pid is None:
        return

    util.pid_kill(db_pid)
    os.remove(conf.get('db_pid'))

    start_time = time.time()
    while 'engine shut down' not in ''.join(log(3)):
        time.sleep(1)
        if (time.time() - start_time) > MAX_TIME:
            raise DBTimeout()


def restart():
    """
    Restart the database.
    """
    stop()
    start()


def init():
    """
    Initialize the database, removes all existing data.
    """
    db.common.init_db()
    for mod_name in ['plugins']:
        __import__('db.' + mod_name).init()


def log(lines=25):
    """
    Get the last lines of the log file.
    """
    try:
        with open(conf.get('db_log')) as fin:
            lines = fin.readlines()[-lines:]
    except IOError:
        lines = ['Log file not yet created.']
    return lines
