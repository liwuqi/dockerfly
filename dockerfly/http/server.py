#!/bin/env python
# -*- coding: utf-8 -*-

import json
from flask import Flask, request

from dockerfly.bin.include import dockerfly_version

dockerfly_app = Flask(__name__)

@dockerfly_app.route('/')
def show_hello():
    return json.dumps({"dockerfly":dockerfly_version})

@dockerfly_app.route('/containers/edit', methods = ['POST', 'PUT', 'DELETE'])
def containers_edit():
    if request.method == 'POST':
        return "ECHO: POST\n"

    elif request.method == 'PUT':
        return "ECHO: PUT\n"

    elif request.method == 'DELETE':
        return "ECHO: DELETE"

@dockerfly_app.route('/containers/status', methods = ['GET'])
def containers_status():
    if request.method == 'GET':
        return "ECHO: GET\n"

@dockerfly_app.route('/containers/control', methods = ['POST'])
def containers_control():
    if request.method == 'POST':
        return "ECHO: POST\n"

def run_server():
    dockerfly_app.run()

if __name__ == '__main__':
    run_server()
