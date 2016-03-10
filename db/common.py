"""
Common code for all database interactions.
"""
from __future__ import absolute_import, print_function
import json

import rethinkdb as r


def connect():
    """
    Return a connection to the database.
    """
    # TODO: Is this an expensive op?
    return r.connect(db='awe')


def init_db():
    """
    Initialize the database.
    """
    with connect() as con:
        try:
            r.db_drop('awe').run(con)
        except r.ReqlOpFailedError:
            pass
        r.db_create('awe').run(con)


def init_table(name, **kwargs):
    """
    Initialize a table in the database.
    """
    with connect() as con:
        try:
            r.table_drop(name).run(con)
        except r.ReqlOpFailedError:
            pass
        r.table_create(name, **kwargs).run(con)


def dump_all():
    """
    Dump all tables contents to stdout.
    """
    with connect() as con:
        for table in r.table_list().run(con):
            print('Table: ' + table)
            print('#' * 50)
            rows = list(r.table(table).run(con))
            print(json.dumps(rows, sort_keys=True, indent=2))
