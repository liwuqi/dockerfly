#!/bin/env python
# -*- coding: utf-8 -*-

"""dockerfly bin tool

Usage:
  dockerfly.py ps
  dockerfly.py gen <config_json>
  dockerfly.py run <config_json>
  dockerfly.py kill <container_id>
  dockerfly.py exec <container_id> <cmd>

Options:
  -h --help             Show this screen.
  --version             Show version.

Example:
    显示所有container              python2.7 dockerfly.py ps
    生成一个container的配置文件    python2.7 dockerfly.py gen centos6.json
    启动一个container              python2.7 dockerfly.py run centos6.json
    停止container                  python2.7 dockerfly.py kill e5d898c10bff
    在container内执行命令          python2.7 dockerfly.py exec e5d898c10bff 'echo hello'
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

    if arguments['exec']:
        container_pid = docker_cli.inspect_container(arguments['<container_id>'])['State']['Pid']
        def process_output(line):
                sys.stdout.write(line)

        p = nsenter('-t', container_pid,
                    '-n', arguments['<cmd>'].split(), _out=process_output)
        p.wait()
