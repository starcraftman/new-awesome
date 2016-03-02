# pylint: disable=missing-docstring,no-self-use
"""
Test db.common
"""
from __future__ import absolute_import, print_function

import rethinkdb as r

import db.common
import util.db_control as dbc


class TestDBCommon(object):
    @classmethod
    def teardown_class(cls):
        dbc.stop()

    def setup(self):
        dbc.start()
        db.common.init_db()

    def test_conn(self):
        assert db.common.conn() is not None

    def test_init_db(self):
        assert 'awe' in list(r.db_list().run(db.common.conn()))

    def test_init_table(self):
        db.common.init_table('plugins')
        assert 'plugins' in list(r.table_list().run(db.common.conn()))
