import requests
from flask import render_template

from flask import Flask, json, request
from flask.ext.restful import reqparse, abort, Api, Resource

dockerflyui_app = Flask(__name__)
dockerflyui_api = Api(dockerflyui_app)

dockerflyd_server = 'http://127.0.0.1:5123'

@dockerflyui_app.route('/')
def home(name=None):
    return render_template('index.html', name=name)

class ContainerList(Resource):
    def get(self):
        return requests.get(dockerflyd_server + '/v1/containers').json()

    def post(self):
        create_containers_json = request.get_json()
        headers = {'content-type': 'application/json'}
        return requests.post(dockerflyd_server + '/v1/containers',
                             data=json.dumps(create_containers_json),
                             headers=headers).json()

class Container(Resource):
    def get(self, container_id):
        return requests.get(dockerflyd_server + '/v1/container/' + container_id).json()

    def delete(self, container_id):
        return requests.delete(dockerflyd_server + '/v1/container/' + container_id).json()

class ContainerActive(Resource):
    def put(self, container_id):
        return requests.put(dockerflyd_server + '/v1/container/' + container_id + '/active').json()

class ContainerInactive(Resource):
    def put(self, container_id):
        return requests.put(dockerflyd_server + '/v1/container/' + container_id + '/inactive').json()

dockerflyui_api.add_resource(ContainerList, '/api/containers')
dockerflyui_api.add_resource(Container, '/api/container/<string:container_id>')
dockerflyui_api.add_resource(ContainerActive, '/api/container/<string:container_id>/active')
dockerflyui_api.add_resource(ContainerInactive, '/api/container/<string:container_id>/inactive')

if __name__ == '__main__':
    dockerflyui_app.run(host='0.0.0.0', port=80, debug=True)
