# pylint: disable=missing-docstring,no-self-use
"""
Test db.common
"""
from __future__ import absolute_import, print_function

import rethinkdb as r

import db.common


def teardown_function(_):
    db.common.init_db()


def test_conn():
    assert db.common.connect() is not None


def test_init_db():
    with db.common.connect() as con:
        assert 'awe' in list(r.db_list().run(con))


def test_init_table():
    db.common.init_table('plugins')
    with db.common.connect() as con:
        assert 'plugins' in list(r.table_list().run(con))
