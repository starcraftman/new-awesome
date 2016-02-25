"""
Common code for all database interactions.
"""
from __future__ import absolute_import, print_function

import rethinkdb as r


def conn():
    """
    Return a connection to the database.
    """
    # TODO: Is this an expensive op? Cache it using a lazy type func?
    return r.connect(db='awe')


def init_db():
    """
    Initialize the database.
    """
    try:
        r.db_drop('awe').run(conn())
    except r.ReqlOpFailedError:
        pass
    r.db_create('awe').run(conn())


def init_table(name):
    """
    Initialize a table in the database.
    """
    try:
        r.table_drop(name).run(conn())
    except r.ReqlOpFailedError:
        pass
    r.table_create(name).run(conn())
