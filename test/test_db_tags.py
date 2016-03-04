# pylint: disable=missing-docstring,no-self-use,attribute-defined-outside-init
"""
Test db.tags
"""
from __future__ import absolute_import

import rethinkdb as r

from db.common import connect
import db.tags


class TestDBPlugins(object):
    def setup(self):
        self.plugin = {
            'id': 'junegunn/vader.vim',
            'tags': ['testing'],
        }
        db.common.init_db()
        db.tags.init()

    @classmethod
    def teardown_class(cls):
        db.common.init_db()

    def test_init(self):
        with connect() as con:
            assert 'tags' in list(r.table_list().run(con))

    def test_add_tags(self):
        db.tags.add_tag(self.plugin['id'], self.plugin['tags'][0])
        with connect() as con:
            entry = list(r.table('tags').run(con))[0]
            assert entry['tag'] == 'testing'
            assert entry['plugins'] == [self.plugin['id']]
