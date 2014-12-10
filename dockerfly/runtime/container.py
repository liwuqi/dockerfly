#!/bin/env python
# -*- coding: utf-8 -*-

import os

from dockerfly.runtime.database import update_db, get_db

def get_all_container_status():
    return get_db('containers')

def get_container_status(container_id):
    for container in get_all_container_status():
        if container_id == container.get('id', None):
            return container
    raise LookupError("The container doesn't exist in dockerfly")

def update_container_status(containers):
    curr_containers = get_all_container_status()
    updating_containers = containers
    new_containers = []

    for curr_container in curr_containers:
        for updating_container in updating_containers:
            if updating_container.get('id', None) and updating_container['id'] == curr_container['id']:
                for k,v in updating_container.items():
                    curr_container[k] = v
        new_containers.append(curr_container)

    update_db(new_containers, 'containers')

def delete_containers(container_ids):
    curr_containers = get_all_container_status()
    new_containers = []
    for index, container in enumerate(curr_containers):
        if container['id'] not in container_ids:
            new_containers.append(container)

    update_db(new_containers, 'containers')
