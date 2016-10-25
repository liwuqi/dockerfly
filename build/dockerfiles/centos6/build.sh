#!/bin/bash

BASE_PATH=$(cd "$(dirname "$0")"; pwd)
docker build -t docker-registry.dev.netis.com.cn:5000/brain/centos:6.6 $BASE_PATH
