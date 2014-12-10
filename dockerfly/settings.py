#!/bin/env python
# -*- coding: utf-8 -*-

import os

#database
default_db_dir = '/var/run/dockerfly'
default_container_db = os.path.join(default_db_dir, 'containers.json')
default_ippool_db = os.path.join(default_db_dir, 'ippool.json')
dbs = [default_container_db, default_ippool_db]
