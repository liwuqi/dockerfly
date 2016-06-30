#!/bin/env python
# -*- coding: utf-8 -*-

import time
import unittest
from sh import ifconfig

from dockerfly.dockerlib.container import Container
from dockerfly.dockerlib.libs import get_all_containers_id
from dockerfly.dockernet.veth import MacvlanEth
from dockerfly.settings import TEST_MOTHER_ETH_NAME

class TestContainer(unittest.TestCase):

    def setUp(self):
        super(TestContainer, self).setUp()
    def test_run_stop_container(self):
        container_id = Container.run('docker.io/memorybox/centos6_sshd',
                                     '/bin/sleep 30',
                                      [
                                         ('testDockerflyv0', TEST_MOTHER_ETH_NAME, '192.168.159.10/24'),
                                         ('testDockerflyv1', TEST_MOTHER_ETH_NAME, '192.168.159.11/24'),
                                         ('testDockerflyv2', TEST_MOTHER_ETH_NAME, '192.168.159.12/24')
                                      ],
                                      '192.168.159.2'
                                     )

        time.sleep(5)
        self.assertTrue(container_id in get_all_containers_id())
        Container.remove(container_id)

    def tearDown(self):
        super(TestContainer, self).tearDown()

