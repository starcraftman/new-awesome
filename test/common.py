# pylint: disable=missing-docstring
"""
Common functionality to be reused among tests.
"""
from __future__ import absolute_import, print_function
import glob
import os
import subprocess as sub

import conf
import util
import util.db_control as dbc

DB_START = os.path.join(util.ROOT, 'conf', '.db_start')


def alive(pid):
    """
    Isolate from utility due to testing catch-22 regarding command/alive.
    """
    return sub.call(['ps', str(pid)], stdout=sub.PIPE, stderr=sub.STDOUT) == 0


def touch_files(root, paths):
    """
    Given a root and a sequence of paths relative the root of form:

        dir1/dir2/file.py

    create any required intermediary directories then write a dummy
    file to basename.

    Returns:
        All created files as absolute paths.
    """
    abs_paths = []

    for relpath in paths:
        path = os.path.join(root, relpath)
        abs_paths.append(path)
        try:
            os.makedirs(os.path.dirname(path))
        except OSError:
            pass
        with open(path, 'w') as fout:
            fout.write('')

    return abs_paths


def save_confs():
    """
    Prevent clobbering existing config during tests.
    """
    fnames = glob.glob(os.path.join(util.ROOT, 'conf', '*.conf'))
    for fname in fnames:
        os.rename(fname, fname + '_bak')


def restore_confs():
    """
    Return any backed up files.
    """
    for fname in glob.glob(os.path.join(util.ROOT, 'conf', '*_bak')):
        os.rename(fname, fname[0:-4])


def env_setup():
    '''
    Setup the testing environment.
    '''
    print('\n-----INIT ENV')
    if os.path.exists(conf.DB_FILE):
        if dbc.alive():
            dbc.stop()
            with open(DB_START, 'w') as fout:
                fout.write('')
        save_confs()

    conf.update_env('test')
    dbc.start()
    print('Using db_root:', conf.get('db_root'))
    print('\n-----INIT ENV FINISHED')


def env_teardown():
    '''
    Teardown the testing environment.
    '''
    print('\n-----DESTROY ENV')
    dbc.stop()

    restore_confs()
    if os.path.exists(DB_START):
        util.delete_it(DB_START)
        dbc.start()
    print('\n-----DESTROY ENV FINISHED')
