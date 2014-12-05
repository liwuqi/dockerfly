#!/bin/env python
# -*- coding: utf-8 -*-

import time
import unittest
from sh import ifconfig

from dockerfly.contrib.dockerlib.container import Container
from dockerfly.contrib.network.veth import MacvlanEth
from dockerfly.contrib.dockerlib.libs import get_all_containers_id

class TestContainer(unittest.TestCase):

    def setUp(self):
        super(TestContainer, self).setUp()
        self._container = Container('centos:centos6',
                                    [
                                        ('testDockerflyv0', 'eth0', '192.168.159.10/24'),
                                        ('testDockerflyv1', 'eth0', '192.168.159.11/24'),
                                        ('testDockerflyv2', 'eth0', '192.168.159.12/24')
                                    ],
                                    '192.168.159.2'
                                )
        self._container.create('/bin/sleep 30')

    def test_run_stop_container(self):
        self._container.run()
        time.sleep(5)
        self.assertTrue(self._container.get_id() in get_all_containers_id())
        self._container.stop()

    def tearDown(self):
        self._container.remove()
        super(TestContainer, self).tearDown()

