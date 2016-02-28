# pylint: disable=missing-docstring,no-self-use,attribute-defined-outside-init
"""
Test db.plugins
"""
from __future__ import absolute_import

import rethinkdb as r

from db.common import conn
import db.plugins
import util.db_control as dbc


class TestDBPlugins(object):
    @classmethod
    def setup_class(cls):
        dbc.start()

    @classmethod
    def teardown_class(cls):
        dbc.stop()

    def setup(self):
        self.plugin_a = {
            'author': 'junegunn',
            'name': 'vim-plug',
            'desc': 'a plugin manager',
        }
        self.plugin_b = {
            'author': 'junegunn',
            'name': 'vader.vim',
            'desc': 'a testing suite',
        }
        self.plugin_c = {
            'author': 'starcraftman',
            'name': 'plug-search',
            'desc': 'plugin to find other plugins'
        }
        for plugin in [self.plugin_a, self.plugin_b, self.plugin_c]:
            plugin['id'] = plugin['author'] + '/' + plugin['name']
        db.common.init_db()
        db.plugins.init()

    def test_plug_id(self):
        expect = self.plugin_a['id']
        del self.plugin_a['id']
        assert self.plugin_a.get('id', None) is None
        assert db.plugins.plug_id(self.plugin_a) == expect
        assert self.plugin_a.get('id', None) is not None

    def test_init(self):
        assert 'plugins' in list(r.table_list().run(conn()))

    def test_exists(self):
        r.table('plugins').insert(self.plugin_a).run(conn())
        assert db.plugins.exists(self.plugin_a)
        assert not db.plugins.exists(self.plugin_b)

    def test_upsert(self):
        db.plugins.upsert(self.plugin_a)
        db.plugins.upsert(self.plugin_a)
        db.plugins.upsert(self.plugin_a)
        plugs = list(r.table('plugins').run(conn()))
        assert len(plugs) == 1
        assert plugs[0]['desc'] == self.plugin_a['desc']

        self.plugin_a['desc'] = 'new line'
        db.plugins.upsert(self.plugin_a)
        plugs = list(r.table('plugins').run(conn()))
        assert len(plugs) == 1
        assert plugs[0]['desc'] == 'new line'
