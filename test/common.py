"""
Common functionality to be reused among tests.
"""
from __future__ import absolute_import, print_function
import glob
import os
import subprocess as sub

import conf
import util


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
    """
    for relpath in paths:
        path = os.path.join(root, relpath)
        try:
            os.makedirs(os.path.dirname(path))
        except OSError:
            pass
        with open(path, 'w') as fout:
            fout.write('')


def save_confs():
    """
    Prevent clobbering existing config during tests.
    """
    fnames = glob.glob(os.path.join(util.ROOT, 'conf', '*.conf'))
    fnames += glob.glob(os.path.join(util.ROOT, 'conf', '*.json'))
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
    save_confs()
    conf.update_env('test')
    print('\n-----INIT ENV FINISHED')


def env_teardown():
    '''
    Teardown the testing environment.
    '''
    print('\n-----DESTROY ENV')
    util.delete_it(conf.get('db_root'))
    restore_confs()
    print('\n-----DESTROY ENV FINISHED')