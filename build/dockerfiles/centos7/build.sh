#!/bin/bash

BASE_PATH=$(cd "$(dirname "$0")"; pwd)
docker build -t docker-registry.dev.netis.com.cn:5000/brain/centos:7.1 $BASE_PATH
