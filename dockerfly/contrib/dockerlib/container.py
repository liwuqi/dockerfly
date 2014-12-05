#!/bin/env python
# -*- coding: utf-8 -*-

import time
import docker as dockerpy

from dockerfly.contrib.network.veth import MacvlanEth
from dockerfly.contrib.dockerlib.libs import run_in_thread, get_all_containers_id

class Container(object):

    def __init__(self, image_name, veths, gateway):
        """create basic container, waiting running

        Args:
            image_name: docker image name
            veths: virtual eths, [('em0v0', 'em0', '192.168.159.10/24'),
                                  ('em1v1', 'em1', '192.168.159.11/24')... )],

                   !!!notify!!!:
                   the first eth will be assigned to the default gateway for container
        """
        self._image_name = image_name
        self._veths = veths
        self._veth_insts = []
        self._gateway = gateway
        self._docker_cli = dockerpy.Client(base_url='unix://var/run/docker.sock')

        self._container_name = "dockerfly_%s_%s" % (self._image_name.replace(':','_'),
                                                    str(int(time.time())))
        self._container = None

    def create(self, run_cmd):
        """create continer by run_cmd"""
        self._container = self._docker_cli.create_container(image=self._image_name,
                                                            command=run_cmd,
                                                            name=self._container_name)

    @run_in_thread
    def run(self):
        """ start container

        Steps:
            run continer
            create virtual eths
            set eths attach to comtainer
        """
        self._docker_cli.start(container=self._container.get('Id'), privileged=True)

        for index, (veth, link_to, ip_netmask) in enumerate(self._veths):
            macvlan_eth = MacvlanEth(veth, ip_netmask, link_to).create()
            container_pid = self.get_pid()

            if index == 0:
                macvlan_eth.attach_to_container(container_pid,
                                                is_route=True, gateway=self._gateway)
            else:
                macvlan_eth.attach_to_container(container_pid)
            self._veth_insts.append(macvlan_eth)

    def stop(self):
        """stop continer"""
        self._docker_cli.stop(self._container.get('Id'))

    def remove(self, force=False):
        """remove eths and continer"""
        if force:
            self._docker_cli.stop(self._container.get('Id'))

        self._docker_cli.remove_container(self._container.get('Id'))

    def get_id(self):
        return self._container.get('Id')

    def get_pid(self):
        return self._docker_cli.inspect_container(self.get_id())['State']['Pid']

