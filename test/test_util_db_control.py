# pylint: disable=missing-docstring,no-self-use
"""
Test the database interface.
"""
from __future__ import absolute_import

import mock
import pytest
import rethinkdb as r

import util.db_control as dbc


class TestDB(object):
    @classmethod
    def teardown_class(cls):
        dbc.start()

    def setup(self):
        dbc.stop()

    def test_alive(self):
        assert not dbc.alive()
        dbc.start()
        assert dbc.alive()

    def test_start(self):
        assert not dbc.alive()
        dbc.start()
        try:
            r.connect()
        except r.errors.ReqlDriverError:
            assert False

    @mock.patch('util.db_control.MAX_TIME', 2)
    @mock.patch('db.common.connect')
    def test_start_timeout(self, mock_conn):
        assert not dbc.alive()
        mock_conn.side_effect = r.errors.ReqlDriverError('')
        with pytest.raises(dbc.DBTimeout):
            dbc.start()

    def test_stop(self):
        assert not dbc.alive()
        dbc.start()
        dbc.stop()
        try:
            r.connect()
            assert False
        except r.errors.ReqlDriverError:
            assert True

    @mock.patch('util.db_control.MAX_TIME', 2)
    def test_stop_raises(self):
        assert not dbc.alive()
        dbc.start()
        with mock.patch('util.db_control.log') as mock_log:
            mock_log.return_value = 'fail'
            with pytest.raises(dbc.DBTimeout):
                dbc.stop()

    def test_restart(self):
        assert not dbc.alive()
        dbc.start()
        dbc.restart()
        try:
            r.connect()
        except r.errors.ReqlDriverError:
            assert False
