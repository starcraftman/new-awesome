"""
Configuration for the whole project.
"""
from __future__ import absolute_import
import json
import os
import tempfile

import util

GCONF_FILE = os.path.join(util.ROOT, 'conf', 'global.conf')
DB_FILE = os.path.join(util.ROOT, 'conf', 'db.conf')
DB_CONF = """
directory={db_root}
log-file={db_log}
pid-file={db_pid}
daemon
direct-io
no-http-admin
""".lstrip()


def update_env(env):
    """
    Regenerates the configuration files for the project.
    """
    conf = gconf_generate(env)

    with open(GCONF_FILE, 'w') as fout:
        json.dump(conf, fout, indent=2, sort_keys=True)

    with open(DB_FILE, 'w') as fout:
        fout.write(DB_CONF.format(**conf))


def gconf_generate(env):
    """
    Generate a new global config for requested environment.
    """
    gconf = {
        'db_root': os.path.join(util.ROOT, 'db', 'rethink'),
        'env': env,
    }
    if env == 'test':
        gconf['db_root'] = tempfile.mkdtemp()
    gconf['db_pid'] = os.path.join(gconf['db_root'], 'pid_file')
    gconf['db_log'] = os.path.join(gconf['db_root'], 'log_file')

    return gconf


def get(key):
    """
    Return the value from the global config.
    """
    # TODO: Cache in memory?
    with open(GCONF_FILE) as fin:
        return json.load(fin)[key]
