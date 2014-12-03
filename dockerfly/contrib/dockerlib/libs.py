#!/bin/env python
# -*- coding: utf-8 -*-

from sh import docker

def getpid(container_name):
    return docker('inspect', '--format',  "'{{ .State.Pid }}'", container_name)
