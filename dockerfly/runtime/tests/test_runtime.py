#!/bin/env python
# -*- coding: utf-8 -*-

import tempfile
import unittest
from sh import ifconfig

from dockerfly.runtime.database import del_db
from dockerfly.runtime.container import (get_status,
                                         get_all_status,
                                         update_status,
                                         add_status,
                                         remove_status,
                                         get_status_db)

class TestRuntime(unittest.TestCase):

    def setUp(self):
        self._test_db_dir = tempfile.mktemp()
        self._containers = [
                {
                    "gateway": "192.168.159.1",
                    "eths": [
                        [
                            "testDockerflyv10",
                            "eth0",
                            "192.168.159.11/24"
                        ]
                    ],
                    "image_name": "172.16.11.13:5000/brain/centos:centos6_sshd",
                    "run_cmd": "/usr/sbin/sshd -D",
                    'id':1,
                    'status':'running',
                    'last_modify_time':1418176930.012
                }, {
                    "gateway": "192.168.159.1",
                    "eths": [
                        [
                            "testDockerflyv20",
                            "eth0",
                            "192.168.159.21/24"
                        ]
                    ],
                    "image_name": "172.16.11.13:5000/brain/centos:centos6_sshd",
                    "run_cmd": "/usr/sbin/sshd -D",
                    'id':2,
                    'status':'running',
                    'last_modify_time':1418176940.012
                }
            ]

    def test_create_container(self):
        add_status(self._containers)
        self.assertEqual(self._containers, get_all_status())

    def test_update_container(self):
        add_status(self._containers)
        update_containers = [
            {
                "gateway": "192.168.159.1",
                "eths": [
                    [
                        "testDockerflyv10",
                        "eth0",
                        "192.168.159.11/24"
                    ]
                ],
                "image_name": "172.16.11.13:5000/brain/centos:centos6_sshd",
                "run_cmd": "/usr/sbin/sshd -D",
                'id':1,
                'status':'stop',
                'last_modify_time':1418176930.012
            }
        ]
        update_status(update_containers)
        self._containers.pop(0)
        self._containers.insert(0, update_containers[0])
        self.assertEqual(get_all_status(), self._containers)

    def test_add_container(self):
        add_status(self._containers)
        add_containers = [
            {
                "gateway": "192.168.159.1",
                "eths": [
                    [
                        "testDockerflyv10",
                        "eth0",
                        "192.168.159.31/24"
                    ]
                ],
                "image_name": "172.16.11.13:5000/brain/centos:centos6_sshd",
                "run_cmd": "/usr/sbin/sshd -D",
                'id':3,
                'status':'running',
                'last_modify_time':1418176930.012
            }
        ]
        add_status(add_containers)
        self._containers.extend(add_containers)
        self.assertEqual(get_all_status(), self._containers)

    def test_remove_container(self):
        add_status(self._containers)
        remove_container_ids = ([1])
        remove_status(remove_container_ids)
        self._containers.pop(0)
        self.assertEqual(get_all_status(), self._containers)

    def tearDown(self):
        del_db(get_status_db())
