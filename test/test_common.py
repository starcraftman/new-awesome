# pylint: disable=missing-docstring
"""
Test test.common
"""
from __future__ import absolute_import, print_function
import glob
import os
import tempfile

import mock

import util
import test.common


def test_touch_files():
    try:
        tempd = tempfile.mkdtemp()
        paths = [
            'file.py',
            'dir1/dir2/file2.py',
            'dir1/dir2/file3.py',
            'dir3/file4.py',
        ]
        test.common.touch_files(tempd, paths)
        for path in paths:
            assert os.path.exists(os.path.join(tempd, path))
    finally:
        util.delete_it(tempd)


@mock.patch('util.ROOT', tempfile.mkdtemp())
def test_save_confs():
    try:
        os.mkdir(os.path.join(util.ROOT, 'conf'))
        paths = [os.path.join(util.ROOT, 'conf', fname) for fname in
                 ('db.conf', 'flask.conf', 'gconf.json')]
        for path in paths:
            with open(path, 'w') as fout:
                fout.write('hello')
            assert os.path.exists(path)

        test.common.save_confs()

        for path in paths:
            assert os.path.exists(path + '_bak')
    finally:
        util.delete_it(util.ROOT)


@mock.patch('util.ROOT', tempfile.mkdtemp())
def test_restore_confs():
    try:
        os.mkdir(os.path.join(util.ROOT, 'conf'))
        paths = [os.path.join(util.ROOT, 'conf', fname) for fname in
                 ('db.conf', 'flask.conf', 'gconf.json')]
        for path in paths:
            with open(path, 'w') as fout:
                fout.write('hello')
            assert os.path.exists(path)

        test.common.save_confs()
        test.common.restore_confs()

        assert len(glob.glob(os.path.join(util.ROOT, 'conf', '*_bak'))) == 0
        for path in paths:
            assert os.path.exists(path)
    finally:
        util.delete_it(util.ROOT)
