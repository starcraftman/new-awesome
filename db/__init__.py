"""
All logic related to managing the database instance.
"""
from __future__ import absolute_import, print_function
import os
import time

import conf
import util


def pid():
    """
    Returns the pid of the rethinkdb server.
    """
    db_pid = None
    if os.path.exists(conf.get('db_pid')):
        with open(conf.get('db_pid')) as fin:
            db_pid = int(fin.readline())

    return db_pid


def status():
    """
    Simply print the status of the database.
    """
    db_pid = pid()
    if db_pid and util.pid_alive(db_pid):
        print('PID:', str(db_pid), 'Root:', conf.get('db_root'))
        print('-' * 60)
        print(''.join(log(5)))
    elif db_pid:
        print('database may have crashed, pid file remains. Call: db stop')
    else:
        print('database not running')


def start():
    """
    Start the database.
    """
    if pid():
        return

    if not os.path.exists(conf.get('db_root')):
        util.command('rethinkdb create -d ' + conf.get('db_root'))
    util.command('rethinkdb serve --config-file ' + conf.DB_FILE)

    while 'Server ready' not in log(1)[0]:
        time.sleep(1)


def stop():
    """
    Stop the database.
    """
    db_pid = pid()
    if db_pid is None:
        return

    util.pid_kill(db_pid)
    try:
        os.remove(conf.get('db_pid'))
    except OSError:
        pass

    while 'Storage engine shut down' not in log(1)[0]:
        time.sleep(1)


def restart():
    """
    Restart the database.
    """
    stop()
    start()


def init():
    """
    (Re)initialize the database, removes all existing data.
    """
    # TODO: Hook all subtables and initialize
    pass


def log(lines=25):
    """
    Get the last lines of the log file.
    """
    with open(conf.get('db_log')) as fin:
        lines = fin.readlines()[-lines:]
    return lines
