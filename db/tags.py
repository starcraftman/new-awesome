"""
Manage the tags table.

Every tag is unique.
Every tag can apply to as many plugins as on site.
"""
from __future__ import absolute_import, print_function

import rethinkdb as r

import db.common


def init():
    """
    Create the table.
    """
    db.common.init_table('tags', primary_key='tag')


def add_tag(plugin_id, tag):
    """
    Add all tags to relevant lists.
    """
    with db.common.connect() as con:
        if r.table('tags').get(tag).run(con) is None:
            r.table('tags').insert({
                'tag': tag,
                'plugins': [plugin_id]
            }).run(con)
        else:
            r.table('tags').get(tag).update(
                {'plugins': r.row['plugins'] + [plugin_id]}
            ).run(con)
