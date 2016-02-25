"""
Manage the tags table.

Constraint, every tag is unique.


"""
from __future__ import absolute_import, print_function

import rethinkdb as r

from db.common import conn


def init():
    """
    Create the table.
    """
    try:
        r.table_drop('tags').run(conn())
    except r.ReqlOpFailedError:
        pass
    r.table_create('tags').run(conn())
    r.table('plugins').index_create('tag').run(conn())
    r.table('plugins').index_wait('tag').run(conn())


def exists(tag):
    """
    Checks if the plugin already in the database.
    """
    matched = list(r.table('tag').filter({'tag': tag}).run(conn()))
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
