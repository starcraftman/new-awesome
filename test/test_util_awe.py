# pylint: disable=missing-docstring
"""
Test the util.awe.py utility script.
"""
from __future__ import absolute_import, print_function
import os
import tempfile

import mock

import util
import util.awe
import test.common as tc


@mock.patch('util.ROOT', tempfile.mkdtemp())
def test_parse_clean_all(mock_print):
    try:
        paths = [
            '.tox/flake8',
            '.venv/bin',
            '__pycache__/log.txt',
            'db/__init__.py',
            'db/__init__.pyc',
            'web/__pycache__/some_cached_file.pyc',
            'test/.cache/file.pyc',
        ]
        tc.touch_files(util.ROOT, paths)
        util.awe.main(['awe', 'clean', '--all'])
        assert sorted(os.listdir(util.ROOT)) == ['db', 'test', 'web']
        assert os.listdir(os.path.join(util.ROOT, 'db')) == ['__init__.py']
        assert os.listdir(os.path.join(util.ROOT, 'test')) == []
        assert os.listdir(os.path.join(util.ROOT, 'web')) == []
        assert mock_print.called
    finally:
        util.delete_it(util.ROOT)
