# pylint: disable=missing-docstring
"""
Test the util module.
"""
from __future__ import absolute_import, print_function
import os
import signal
import tempfile

import pytest

import util
import test.common as tc

TRAP_SH = os.path.join(util.ROOT, 'test', 'trap.sh')


def test_root():
    assert os.path.exists(os.path.join(util.ROOT, 'Vagrantfile'))


def test_glob_recursively():
    try:
        tempd = tempfile.mkdtemp()
        paths = [
            'match2.py',
            'db/db.conf',
            'dir1/dir2/match.py',
            'web/static/main.css',
        ]
        tc.touch_files(tempd, paths)
        expect = [os.path.join(tempd, paths[0]),
                  os.path.join(tempd, paths[2])]
        assert util.glob_rec(tempd, r'.*\.py') == expect
    finally:
        util.delete_it(tempd)


def test_pid_wait_on():
    pid = util.command(TRAP_SH, wait=False)
    assert tc.alive(pid)
    util.pid_kill(pid, signal.SIGKILL)
    util.pid_wait_on(pid)
    assert not tc.alive(pid)


def test_pid_wait_on_timeout():
    pid = util.command(TRAP_SH, wait=False)
    assert tc.alive(pid)
    with pytest.raises(OSError):
        util.pid_wait_on(pid)


def test_pid_kill():
    pid = util.command(TRAP_SH, wait=False)
    assert tc.alive(pid)
    util.pid_kill(pid, signal.SIGKILL)
    util.pid_wait_on(pid)
    assert not tc.alive(pid)


def test_pid_kill_raises():
    with pytest.raises(OSError):
        assert tc.alive(1)
        util.pid_kill(1)


def test_pid_alive():
    pid = util.command(TRAP_SH, wait=False)
    assert util.pid_alive(pid)
    util.pid_kill(pid)
    util.pid_wait_on(pid)
    assert not util.pid_alive(pid)


def test_pid_alive_invalid():
    with pytest.raises(ValueError):
        util.pid_alive(-5)


def test_command_dir():
    ndir = os.path.expanduser('~')
    ret = util.command('pwd', cwd=ndir)
    assert ret == (0, ndir + "\n")


def test_command_sync():
    ret = util.command('echo "Hello"')
    assert ret == (0, "Hello\n")


def test_command_async():
    pid = util.command(TRAP_SH, wait=False)
    assert tc.alive(pid)
    util.pid_kill(pid)
    util.pid_wait_on(pid)
    assert not tc.alive(pid)


def test_delete_it():
    try:
        temp = tempfile.NamedTemporaryFile(delete=False)
        temp.write('Hello world.')
        tempd = tempfile.mkdtemp()
        with open(os.path.join(tempd, 'test'), 'w') as fout:
            fout.write('Hello again!')
        paths = [temp.name, tempd]

        for path in paths:
            assert os.path.exists(path)
            util.delete_it(path)
            assert not os.path.exists(path)
    finally:
        for path in paths:
            util.delete_it(path)
