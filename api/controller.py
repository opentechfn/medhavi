import json

import flask
from flask import Blueprint
from flask import Flask
from flask import jsonify
from flask import make_response
from flask import request
from oslo_utils import uuidutils
from webob import exc

from common import exceptions
from db import api
from db.models import db
from json_parser import JsonParser
from migrate import app as application


class Controller():

    @application.route('/data', methods = ['POST'])
    def post():
        content = request.get_json()
        with open('temp.json', 'w') as f:
            json.dump(content, f)
        json_obj = JsonParser("temp.json")

        json_obj.validate_json_data_type(content)
        json_data = json_obj.parse_json_data()
        
        ml_uuid = uuidutils.generate_uuid()
        url = content['DataURL']
        ml_lib = content['variables']['mlLib']
        is_form_cluster = content['variables']['isFormCluster']
        storage_name = content['variables']['storageAccountName']
        storage_type = content['variables']['storageAccountType']

        api.mldata_create(ml_uuid, url, ml_lib, is_form_cluster,
                          storage_name, storage_type)

        resources = content['resource']
        for res in resources:
            res_uuid = uuidutils.generate_uuid()
	    resource_type = res.get('InfrastrctureType')
            provider = res.get('provider')
            if res.get('APIEndpoint'):
                endpoint = res.get('APIEndpoint')
            if res.get('PublicEndpoint'):
                endpoint = res.get('PublicEndpoint')
            username = res.get('username')
            password = res.get('password')
            token = res.get('token')
	    availability_zone = res.get('availabilityZone')
	    region = res.get('Region')

            api.resource_create(res_uuid, resource_type, provider, endpoint,
                                username, password, token, availability_zone,
				region)

            if res['NodeList']:
                for node in res['NodeList']:
                    uuid = uuidutils.generate_uuid()
                    resource_id = res_uuid
                    node_ip = node.get('NodeIP')
                    username = node.get('Username')
                    password = node.get('Password')
                    api.node_create(uuid, resource_id, node_ip,
                                    username, password)

        return json.dumps(201, {'ContentType':'application/json'})

    @application.route("/resource/<id>", methods=["GET"])
    def get_resource(id):
        try:
            result = api.resource_detail(id)
            return make_response(jsonify(result), 200)
        except exceptions.ResourceNotFound:
            msg = "Can not find requested resource: %s" % id
            return exc.HTTPNotFound(explanation=msg)

    @application.route("/resource", methods=["GET"])
    def get_all_resources():
        return api.get_all_resources()

    @application.route("/resource/<id>", methods=["DELETE"])
    def resource_delete(id):
        try:
            api.resource_delete(id)
            return {"status": 'success'}, 204
        except exceptions.ResourceNotFound:
            msg = "Can not find requested resource: %s" % id
            return exc.HTTPNotFound(explanation=msg)
 
    @application.route("/mldata/<id>", methods=["GET"])
    def get_mldata(id):
        try:
            result = api.mldata_detail(id)
            return make_response(jsonify(result))
        except exceptions.MLDataNotFound:
            msg = "Can not find requested MLData: %s" % id
            return exc.HTTPNotFound(explanation=msg)

    @application.route("/mldata", methods=["GET"])
    def get_all_mldata():
        return api.get_all_mldata()

    @application.route("/mldata/<id>", methods=["DELETE"])
    def mldata_delete(id):
        try:
            api.mldata_delete(id)
            return {"status": 'success'}, 204
        except exceptions.MLDataNotFound:
            msg = "Can not find requested MLData: %s" % id
            return exc.HTTPNotFound(explanation=msg)

    @application.route("/node/<id>", methods=["GET"])
    def get_node(id):
        try:
            result = api.node_detail(id)
            return make_response(jsonify(result), 200)
        except exceptions.NodeNotFound:
            msg = "Can not find requested node: %s" % id
            return exc.HTTPNotFound(explanation=msg)

    @application.route("/node", methods=["GET"])
    def get_all_nodes():
        return api.get_all_nodes()

    @application.route("/node/<id>", methods=["DELETE"])
    def node_delete(id):
        try:
            api.node_delete(id)
            return {"status": 'success'}, 204
        except exceptions.NodeNotFound:
            msg = "Can not find requested node: %s" % id
            return exc.HTTPNotFound(explanation=msg)
