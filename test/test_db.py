# pylint: disable=missing-docstring,no-self-use
"""
Test the database interface.
"""
from __future__ import absolute_import

import mock
import pytest
import rethinkdb as r

import db
import util


class TestDB(object):
    def setup(self):
        db.stop()

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

    @mock.patch('db.MAX_TIME', 2)
    @mock.patch('db.log')
    def test_start_timeout(self, mock_log):
        assert not db.pid()
        mock_log.return_value = 'fail'
        with pytest.raises(db.DBTimeout):
            db.start()

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

    @mock.patch('db.MAX_TIME', 2)
    def test_stop_raises(self):
        assert not db.pid()
        db.start()
        with mock.patch('db.log') as mock_log:
            mock_log.return_value = 'fail'
            with pytest.raises(db.DBTimeout):
                db.stop()

    def test_restart(self):
        assert not db.pid()
        db.start()
        db.restart()
        try:
            r.connect().repl()
        except r.errors.ReqlDriverError:
            assert False
        assert util.pid_alive(db.pid())
