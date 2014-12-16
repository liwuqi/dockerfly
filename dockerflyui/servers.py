import requests
from flask import render_template

from flask import Flask, json, request
from flask.ext.restful import reqparse, abort, Api, Resource

dockerflyui_app = Flask(__name__)
dockerflyui_api = Api(dockerflyui_app)

dockerflyd_server = 'http://192.168.159.147:5000'

@dockerflyui_app.route('/')
def home(name=None):
    return render_template('index.html', name=name)

class ContainerList(Resource):
    def get(self):
        return requests.get(dockerflyd_server + '/v1/containers').json()

    def post(self):
        create_containers_json = request.get_json()
        return request.post(dockerflyd_server + '/v1/containers', data= create_containers_json).json()

dockerflyui_api.add_resource(ContainerList, '/api/containers')

if __name__ == '__main__':
    dockerflyui_app.run(host='0.0.0.0', port=80, debug=True)
