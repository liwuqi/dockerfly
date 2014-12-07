#!/bin/env python
# -*- coding: utf-8 -*-

"""dockerfly bin tool

Usage:
  dockerfly.py ps
  dockerfly.py gen <config_json>
  dockerfly.py run <config_json>
  dockerfly.py get <container_id>

Options:
  -h --help             Show this screen.
  --version             Show version.

Example:
    show all containers             python2.7 dockerfly.py ps
    generate container config       python2.7 dockerfly.py gen centos6.json
    start container                 python2.7 dockerfly.py run centos6.json
    remove container                python2.7 dockerfly.py kill e5d898c10bff
    getpid container pid            python2.7 dockerfly.py getpid e5d898c10bff
"""

import os
import sys
import json
from sh import docker, nsenter
from docopt import docopt
import docker as dockerpy

try:
    import dockerfly
except ImportError:
    sys.path.insert(0, os.path.abspath(os.path.join(__file__, '../../../')))

from dockerfly.contrib.dockerlib.container import Container

if __name__ == '__main__':
    arguments = docopt(__doc__, version='dockerfly 0.1')
    docker_cli = dockerpy.Client(base_url='unix://var/run/docker.sock')

    container_json_exp = [{
            'image_name':'centos:centos6',
            'run_cmd': '/bin/sleep 30',
            'eths':
            [
               ('testDockerflyv0', 'eth0', '192.168.159.10/24'),
               ('testDockerflyv1', 'eth0', '192.168.159.11/24'),
               ('testDockerflyv2', 'eth0', '192.168.159.12/24')
            ],
            'gateway':'192.168.159.2'
        }]

    if arguments['ps']:
        print docker('ps')

    if arguments['gen']:
        with open(arguments['<config_json>'], 'w') as config:
            json.dump(container_json_exp, config, indent=4, encoding='utf-8')

    if arguments['run']:
        with open(arguments['<config_json>'], 'r') as config:
            container_json = json.load(config, encoding='utf-8')
            for container in container_json:
                Container.run(container['image_name'],
                              container['run_cmd'],
                              container['eths'],
                              container['gateway']
                            )
    if arguments['kill']:
        Container.remove(arguments['<container_id>'])

    if arguments['get']:
        print docker_cli.inspect_container(arguments['<container_id>'])['State']['Pid']
