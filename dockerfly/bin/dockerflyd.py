#!/bin/env python
# -*- coding: utf-8 -*-

import os
import grp
import signal
import daemon
import lockfile

import include
from dockerfly.settings import dockerfly_version
from dockerfly.http.server import run_server

def dockerflyd_setup():
    pass

def dockerflyd_cleanup():
    pass

def dockerflyd_reload_config():
    pass

context = daemon.DaemonContext(
    working_directory='/var/lib/dockerfly',
    umask=0o002,
    pidfile=lockfile.FileLock('/var/run/dockerflyd.pid'),
    )

context.signal_map = {
    signal.SIGTERM: dockerflyd_cleanup,
    signal.SIGHUP: 'terminate',
    signal.SIGUSR1: dockerflyd_reload_config,
    }

mail_gid = grp.getgrnam('mail').gr_gid
context.gid = mail_gid

#important_file = open('spam.data', 'w')
#interesting_file = open('eggs.data', 'w')
#context.files_preserve = [important_file, interesting_file]

if __name__ == '__main__':
    dockerflyd_setup()

    with daemon.DaemonContext():
        run_server()

