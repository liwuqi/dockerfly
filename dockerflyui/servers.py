#!/bin/env python
# -*- coding: utf-8 -*-

"""
dockerflyui run server scripts

Usage:
  servers.py <ip> <port> [--dockerflyd=<ip:port>]

Options:
  -h --help                 Show this screen.
  --dockerflyd=<ip:port>    Set dockerflyd ip and port [default: 127.0.0.1:5123]

Example:
    python dockerflyui/servers.py 0.0.0.0 80
    python dockerflyui/servers.py 0.0.0.0 80 --dockerflyd 127.0.0.1:5123
"""

import os
import requests
from flask import render_template
from docopt import docopt
import docker as dockerpy

from flask import Flask, json, request, jsonify
from flask.ext.restful import Api, Resource

dockerflyui_app = Flask(__name__)
dockerflyui_api = Api(dockerflyui_app)


dockerflyd_server = 'http://127.0.0.1:5123'
docker_cli = dockerpy.Client(base_url='unix://var/run/docker.sock')

@dockerflyui_app.route('/')
def home(name=None):
    return render_template('index.html', name=name)

class ImageList(Resource):
    def get(self):
        return jsonify(
                        {
                            'images':
                            [item['RepoTags'][0] for item in docker_cli.images()]
                        }
                    )

class ContainerList(Resource):
    def get(self):
        response = requests.get(dockerflyd_server + '/v1/containers')
        return response.json(), response.status_code

    def post(self):
        create_containers_json = request.get_json()
        headers = {'content-type': 'application/json'}
        response = requests.post(dockerflyd_server + '/v1/containers',
                             data=json.dumps(create_containers_json),
                             headers=headers)
        return response.json(), response.status_code


class Container(Resource):
    def get(self, container_id):
        response = requests.get(dockerflyd_server + '/v1/container/' + container_id)
        return response.json(), response.status_code

    def delete(self, container_id):
        response = requests.delete(dockerflyd_server + '/v1/container/' + container_id)
        return response.json(), response.status_code

class ContainerActive(Resource):
    def put(self, container_id):
        response = requests.put(dockerflyd_server + '/v1/container/' + container_id + '/active')
        return response.json(), response.status_code

class ContainerInactive(Resource):
    def put(self, container_id):
        response = requests.put(dockerflyd_server + '/v1/container/' + container_id + '/inactive')
        return response.json(), response.status_code

dockerflyui_api.add_resource(ImageList, '/api/images')
dockerflyui_api.add_resource(ContainerList, '/api/containers')
dockerflyui_api.add_resource(Container, '/api/container/<string:container_id>')
dockerflyui_api.add_resource(ContainerActive, '/api/container/<string:container_id>/active')
dockerflyui_api.add_resource(ContainerInactive, '/api/container/<string:container_id>/inactive')

def runweb(host, port, daemon_server):
    global dockerflyd_server
    dockerflyd_server = os.path.join('http://', daemon_server)
    dockerflyui_app.run(host=host, port=port, debug=False)

if __name__ == '__main__':
    arguments = docopt(__doc__)
    runweb(arguments['<ip>'], int(arguments['<port>']), arguments['--dockerflyd'])
