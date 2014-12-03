#!/bin/env python
# -*- coding: utf-8 -*-

from sh import docker

class Container(object):

    def __init__(self, image_name, veths):
        self._image_name = image_name
        self._veths = veths

