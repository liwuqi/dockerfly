#!/bin/env python
# -*- coding: utf-8 -*-

import os
import grp
import logging
import signal
import daemon
import lockfile

import include
from dockerfly.settings import dockerfly_version
from dockerfly.http.server import run_server

working_directory = '/var/run/dockerfly'
logging_directory = os.path.join(working_directory, 'log')

if not os.path.exists(working_directory):
    os.mkdir(working_directory)
if not os.path.exists(logging_directory):
    os.mkdir(logging_directory)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(os.path.join(logging_directory, 'dockerflyd.log'))
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

pid_file = os.path.join(working_directory, 'dockerflyd.pid.lock')

def dockerflyd_setup():
    if os.path.exists(pid_file):
        logger.error("{} has already existed".format(pid_file))

def dockerflyd_cleanup():
    if os.path.exists(pid_file):
        os.remove(pid_file)

def dockerflyd_reload_config():
    pass

context = daemon.DaemonContext(
    working_directory=working_directory,
    umask=0o002,
    pidfile=lockfile.FileLock(os.path.join(working_directory, 'dockerflyd.pid')),
    files_preserve = [fh.stream,],
)

context.signal_map = {
    signal.SIGTERM: dockerflyd_cleanup,
    signal.SIGHUP: 'terminate',
    signal.SIGUSR1: dockerflyd_reload_config,
    }

mail_gid = grp.getgrnam('mail').gr_gid
context.gid = mail_gid

def rundaemon(host, port):
    dockerflyd_setup()

    with context:
        run_server(host=host, port=port, debug=True)

if __name__ == '__main__':
    rundaemon(host='0.0.0.0', port=5123)

