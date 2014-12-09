#!/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask

dockerfly_app = Flask(__name__)

@dockerfly_app.route('/')
def hello_world():
    return 'hello, world'

def run_server():
    dockerfly_app.run()

if __name__ == '__main__':
    run_server()
