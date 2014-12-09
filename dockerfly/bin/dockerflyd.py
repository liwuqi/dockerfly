#!/bin/env python
# -*- coding: utf-8 -*-

import daemon

from include import dockerfly_version
from dockerfly.http.server import run_server

with daemon.DaemonContext():
    run_server()

