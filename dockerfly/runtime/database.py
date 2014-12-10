#!/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import time
import shutil

default_db_dir = '/var/run/dockerfly'
default_container_db = os.path.join(default_db_dir, 'containers.json')
dbs = [default_container_db]

def init_db(func):
    if not os.path.exists(default_db_dir):
        os.mkdir(default_db_dir)
    for db in dbs:
        if not os.path.exists(db):
            with open(db, 'w') as db_file:
                json.dump({}, db_file)
    return func

@init_db
def update_db(content, db_name='containers', db_dir=default_db_dir):
    db_file = os.path.join(db_dir, db_name)
    lock_file = os.path.join(db_file, '.json.lock')
    while True:
        if os.path.exists(lock_file):
            time.sleep(0.1)
        else:
            break

    #lock update op
    open(lock_file, 'a').close()
    with open(db_file, 'w') as db:
        json.dump(content, db)
    os.remove(lock_file)

@init_db
def get_db(db_name='containers', db_dir=default_db_dir):
    db_file = os.path.join(db_dir, db_name)
    with open(db_file, 'a') as db:
        return json.load(db)
