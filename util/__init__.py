"""
Anything of general utility goes here.
"""
from __future__ import absolute_import
import os
import re
import shlex
import shutil
import signal
import subprocess as sub
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def glob_rec(root, pattern, ignore_dirs=None):
    """
    Recursively walk down from root searching for files or folders
    matching the regex pattern.

    Args:
        root: An absolute path to start in.
        pattern: Any valid matcher for files.
        ignore_dirs: Ignore all directories matching.

    Returns:
        A list of matched absolute paths.
    """
    matcher = re.compile(pattern)
    matched = []
    if ignore_dirs is None:
        ignore_dirs = []

    for dirname, subdirs, fnames in os.walk(root):
        for idir in ignore_dirs:
            if idir in subdirs:
                subdirs.remove(idir)
        matched += [os.path.join(dirname, fname) for fname in
                    fnames + subdirs if re.match(matcher, fname)]

    return matched


def command(cmd, wait=True, **kwargs):
    """
    Execute the command as a subprocess, synchronously or asynchronously.

    Args:
        cmd: The string cmd to execute. If shlex would not
            handle it well, pass a list of strings.
        wait: If True, wait for command completion.
        kwargs: Any valid Popen constructor keyword.

    Returns:
        wait == True: (returncode, output)
        wait == False: process_id
    """
    pargs = {
        'preexec_fn': os.setsid,
        'stderr': sub.STDOUT,
        'stdout': sub.PIPE,
    }
    pargs.update(kwargs)
    proc = sub.Popen(shlex.split(cmd) if isinstance(cmd, type('')) else cmd,
                     **pargs)
    if wait:
        proc.wait()
        return (proc.returncode, proc.stdout.read())
    else:
        return proc.pid


def delete_it(path):
    """
    File or folder, it is deleted.

    Args:
        path: path to a file or dir
    """
    try:
        shutil.rmtree(path)
    except OSError:
        try:
            os.remove(path)
        except OSError:
            pass


def pid_alive(pid):
    """
    Checks if a pid exists on the system.
    """
    if pid < 1:
        raise ValueError('Invalid PID: ' + str(pid))

    # ps exits with 1 if pid invalid
    return command('ps ' + str(pid))[0] == 0


def pid_kill(pid, sig=signal.SIGTERM):
    """
    Send signal to a process, by default SIGTERM.

    Raises:
        AssertionError: Pid wasn't valid.
        OSError: Some OS error occured, pid likely not dead.
    """
    assert pid_alive(pid)
    os.kill(pid, sig)


def pid_wait_on(pid, timeout=3, step=0.5):
    """
    Wait on the pid to quit. If timeout exceded raise OSError.

    Args:
        pid: A valid pid on the system.
        step: Check if pid alive every step seconds.
        timeout: After timeout seconds, raise Error.
    """
    cnt = 0
    while cnt < timeout:
        cnt += step
        time.sleep(step)
        if not pid_alive(pid):
            return

    raise OSError('PID still alive ' + str(pid))
