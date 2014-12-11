#!/bin/env python
# -*- coding: utf-8 -*-

import json
from flask import Flask, request
from flask.ext.restful import reqparse, abort, Api, Resource

from dockerfly.settings import dockerfly_version

dockerfly_app = Flask(__name__)
dockerfly_api = Api(dockerfly_app)

containers = []

def abort_if_container_doesnt_exist(container_id):
    if container_id not in containers:
        abort(404, message="Container {} doesn't exist".format(container_id))

class Version(Resource):
    def get(self):
        return {'version':dockerfly_version}

class ContainerList(Resource):
    def get(self):
        return {'all':'bbbbbbbbbbbbb'}

    def post(self):
        return {}

class Container(Resource):
    def get(self, container_id):
        abort_if_container_doesnt_exist(container_id)
        return containers[container_id]

    def delete(self, container_id):
        return {}

class ContainerActive(Resource):
    def post(self, container_id):
        return {}

class ContainerInactive(Resource):
    def post(self, container_id):
        return {}

class ContainerTaskList(Resource):
    def post(self, container_id):
        return {}

class ContainerTask(Resource):
    def get(self, task_id):
        return {}

    def delete(self, task_id):
        return {}

dockerfly_api.add_resource(Version, '/v1/version')
dockerfly_api.add_resource(ContainerList, '/v1/container')
dockerfly_api.add_resource(Container, '/v1/container/<string:container_id>')
dockerfly_api.add_resource(Container, '/v1/container/active')
dockerfly_api.add_resource(Container, '/v1/container/inactive')
dockerfly_api.add_resource(ContainerTaskList, '/v1/container/task')
dockerfly_api.add_resource(ContainerTask, '/v1/container/task/<string:task_id>')

def run_server():
    dockerfly_app.run()

if __name__ == '__main__':
    run_server()
