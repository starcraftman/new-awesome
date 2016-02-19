# pylint: disable=missing-docstring
"""
Test conf
"""
from __future__ import absolute_import
import json
import tempfile

import mock

import conf
import util


@mock.patch('conf.GCONF_FILE', tempfile.NamedTemporaryFile().name)
@mock.patch('conf.DB_FILE', tempfile.NamedTemporaryFile().name)
def test_update_env():
    try:
        conf.update_env('test')
        with open(conf.GCONF_FILE) as fin:
            gconf = fin.read()
            assert '"env": "test"' in gconf
            assert 'db_root": "/tmp/tmp' in gconf
        with open(conf.DB_FILE) as fin:
            dbconf = fin.read()
            assert 'directory=/tmp/tmp' in dbconf
            assert 'daemon' in dbconf
    finally:
        util.delete_it(conf.get('db_root'))
        util.delete_it(conf.GCONF_FILE)
        util.delete_it(conf.DB_FILE)


def test_gconf_generate():
    try:
        gconf = conf.gconf_generate('test')
        assert gconf['env'] == 'test'
        assert '/tmp/tmp' in gconf['db_root']
    finally:
        util.delete_it(gconf['db_root'])


@mock.patch('conf.GCONF_FILE', tempfile.NamedTemporaryFile().name)
def test_get():
    try:
        with open(conf.GCONF_FILE, 'w') as fout:
            json.dump({'hello': 'world'}, fout)
        assert conf.get('hello') == 'world'
    finally:
        util.delete_it(conf.GCONF_FILE)
