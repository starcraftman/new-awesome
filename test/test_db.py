# pylint: disable=missing-docstring,no-self-use
"""
Test the database interface.
"""
from __future__ import absolute_import

import rethinkdb as r

import db
import util


class TestDB(object):
    def teardown(self):
        db.stop()

    def test_start(self):
        assert not db.pid()
        db.start()
        try:
            r.connect()
        except r.errors.ReqlDriverError:
            assert False
        assert util.pid_alive(db.pid())

    def test_stop(self):
        assert not db.pid()
        db.start()
        db.stop()
        try:
            r.connect().repl()
            assert False
        except r.errors.ReqlDriverError:
            assert True
        assert not db.pid()

    def test_restart(self):
        assert not db.pid()
        db.start()
        db.restart()
        try:
            r.connect().repl()
        except r.errors.ReqlDriverError:
            assert False
        assert util.pid_alive(db.pid())
