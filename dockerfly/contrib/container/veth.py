#!/bin/env python
# -*- coding: utf-8 -*-

class VEth(object):
    """support ip link add vethxxx ..."""

    def __init__(self, name, ip, link_to):

        self._veth_name = name
        self._ip = ip
        self._link_to = link_to

    def add(self):
        raise NotImplementedError

    def attach_to_container(self):
        raise NotImplementedError

class MacvlanEth(VEth):
    """add a macvlan eth to net namespace and attach to container

    as the same as exec commands below:

        ip link add em0v0 link em0 type macvlan mode bridge
        ip link set netns $(docker container pid) em0v0
        nsenter -t $(docker container pid)
    """
