# pylint: disable=missing-docstring,no-self-use
"""
Test the database interface.
"""
from __future__ import absolute_import

import mock
import pytest
import rethinkdb as r

import util
import util.db_control as dbc


class TestDB(object):
    def setup(self):
        dbc.stop()

    def teardown(self):
        dbc.stop()

    def test_start(self):
        assert not dbc.pid()
        dbc.start()
        try:
            r.connect()
        except r.errors.ReqlDriverError:
            assert False
        assert util.pid_alive(dbc.pid())

    @mock.patch('util.db_control.MAX_TIME', 2)
    @mock.patch('util.db_control.log')
    def test_start_timeout(self, mock_log):
        assert not dbc.pid()
        mock_log.return_value = 'fail'
        with pytest.raises(dbc.DBTimeout):
            dbc.start()

    def test_stop(self):
        assert not dbc.pid()
        dbc.start()
        dbc.stop()
        try:
            r.connect().repl()
            assert False
        except r.errors.ReqlDriverError:
            assert True
        assert not dbc.pid()

    @mock.patch('util.db_control.MAX_TIME', 2)
    def test_stop_raises(self):
        assert not dbc.pid()
        dbc.start()
        with mock.patch('util.db_control.log') as mock_log:
            mock_log.return_value = 'fail'
            with pytest.raises(dbc.DBTimeout):
                dbc.stop()

    def test_restart(self):
        assert not dbc.pid()
        dbc.start()
        dbc.restart()
        try:
            r.connect().repl()
        except r.errors.ReqlDriverError:
            assert False
        assert util.pid_alive(dbc.pid())
