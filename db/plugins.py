"""
Manage the plugins table.

Constraint, every ('author', 'name') tuple is unique in table.
Primary key is 'author/name' string, a concatenation of two fields.

Possible fields on plugin:
    'id': String. Required. Form: author/name
    'author': String. Required.
    'name': String. Required.
    'desc': String. Required.
    'tags': List. Required.

    'is_fork': String. False if ommitted. If true, points to parent. Optional
    'fork': String. An active fork that has replaced the original. Optional.
    'opts': A dictionary of standard opts to make it work. Optional.
    'project': String. URL of the project. Ommitted then assume github.
               https://github.com/author/repo .
    'alts': List. Alternative plugins, substantial overlap in function.
"""
from __future__ import absolute_import, print_function

import rethinkdb as r

from db.common import conn, init_table


def init():
    """
    Create the table.
    """
    init_table('plugins')
    r.table('plugins').index_create('author').run(conn())
    r.table('plugins').index_wait('author').run(conn())


def exists(plugin):
    """
    Checks if the plugin already in the database.
    """
    return r.table('plugins').get(plug_id(plugin)).run(conn()) is not None


def plug_id(plugin):
    """
    Return the id, that is the primary key of a plugin.
    Modifies the dictionary to ensure the 'id' key is set.

    Returns:
        The id of the plugin.
    """
    plugin['id'] = plugin['author'] + '/' + plugin['name']
    return plugin['id']


def upsert(plugin):
    """
    Insert into plugins table. If it exists, update the entry.
    """
    if exists(plugin):
        r.table('plugins').get(plug_id(plugin)).update(plugin).run(conn())
    else:
        r.table('plugins').insert(plugin).run(conn())
