"""
Manage the plugins table.

Constraint, every ('author', 'name') tuple is unique in table.

Possible fields on plugin:
    'author': String. Required.
    'name': String. Required.
    'desc': String. Required.
    'tags': List. Required.

    'is_fork': String. False if ommitted. If true, points to parent. Optional
    'fork': There is an active fork that has replaced the original. Optional.
    'opts': A dictionary of standard opts to make it work. Optional.
    'project': URL of the project. Ommitted then assume github.
               https://github.com/author/repo .
    'alts': Alternative plugins like this one, substantial overlap in function.
"""
from __future__ import absolute_import, print_function

import rethinkdb as r

from db.common import conn


def init():
    """
    Create the table.
    """
    try:
        r.table_drop('plugins').run(conn())
    except r.ReqlOpFailedError:
        pass
    r.table_create('plugins').run(conn())
    sec_ind = [r.row['author'], r.row['name']]
    r.table('plugins').index_create('key', sec_ind).run(conn())
    r.table('plugins').index_wait('key').run(conn())


def exists(plugin):
    """
    Checks if the plugin already in the database.
    """
    matched = list(r.table('plugins').filter({
        'author': plugin['author'],
        'name': plugin['name']
    }).run(conn()))
    return len(matched) != 0


def insert(plugin):
    """
    Insert into plugins table.
    """
    if exists(plugin):
        update(plugin)
    else:
        r.table('plugins').insert(plugin).run(conn())


def update(plugin):
    """
    Update the entry for plugin.
    """
    r.table('plugins').filter({
        'author': plugin['author'],
        'name': plugin['name']
    }).update(plugin).run(conn())
