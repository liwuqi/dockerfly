#!/bin/env python
# -*- coding: utf-8 -*-

import time
from sh import docker

from dockerfly.contrib.network.veth import MacvlanEth
from .libs import getpid

class Container(object):

    def __init__(self, image_name, veths):
        """create basic container, waiting running

        Args:
            image_name: docker image name
            veths: virtual eths, [('em0v0', 'em0'), ('em1v1', 'em1')... )],
                   the first eth will be default gateway for container
        """
        self._image_name = image_name
        self._veths = veths
        self._container_name = "dockerfly_%s_%s" % (self._image_name, str(int(time.time())))

    def run(self, run_cmd, *args):
        """ start container

        Steps:
            run continer by run_cmd
            create virtual eths
            set eths attach to comtainer
        """
        docker('run', '--privileged', '--name', self._container_name,
                args, self._image_name, run_cmd)

        for veth, link_to, ip_netmask in self._veths:
            macvlan_eth = MacvlanEth(veth, ip_netmask, link_to).create()
            macvlan_eth.attach_to_container(getpid(self._container_name))


