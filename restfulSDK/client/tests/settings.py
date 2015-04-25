#!/usr/bin/env python
#  -*- coding: utf-8 -*-

TEST_VM_HOST = {'name':'test_create_vm1_for_dockerfly',
                'ip':'192.168.1.100/24',
                'project':'centos6',
                'desc':'unit test for dockerfly',
                'gateway':'192.168.1.1',
                'dockerflyd_server':'http://192.168.1.10:5123/v1/'
                }

try:
    from local_settings import *
except ImportError:
    pass
