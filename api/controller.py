import json

from flask import jsonify
from flask import make_response
from flask import request
from oslo_config import cfg
import oslo_messaging as om
from oslo_utils import uuidutils
from webob import exc

import config
from common import exceptions
from json_parser import JsonParser
from migrate import app as application


# Invoke "get_transport". This call will set default Configurations required
# to Create Messaging Transport
transport = om.get_transport(cfg.CONF)

# Set/Override Configurations required to Create Messaging Transport
cfg.CONF.set_override('transport_url', config.transport_url)

# Create Messaging Transport
transport = om.get_transport(cfg.CONF)

# Create Target (Exchange, Topic and Server to listen on)
target = om.Target(topic='testme')

client = om.RPCClient(transport, target)


class Controller():
    """Controller for MLData, resources and node."""

    @application.route('/data', methods=['POST'])
    def post():
        with application.app_context():
            content = request.get_json()
            with open('temp.json', 'w') as f:
                json.dump(content, f)
            json_obj = JsonParser("temp.json")

            json_obj.validate_json_data_type(content)
            json_obj.parse_json_data()

            ctxt = {}
            ml_uuid = uuidutils.generate_uuid()
            url = content['DataURL']
            ml_lib = content['variables']['mlLib']
            is_form_cluster = content['variables']['isFormCluster']
            storage_name = content['variables']['storageAccountName']
            storage_type = content['variables']['storageAccountType']

            client.call(ctxt, 'mldata_create', uuid=ml_uuid, url=url,
                        ml_lib=ml_lib, is_form_cluster=is_form_cluster,
                        storage_name=storage_name, storage_type=storage_type)

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

                client.call(ctxt, 'resource_create', uuid=res_uuid,
                            resource_type=resource_type, provider=provider,
                            endpoint=endpoint, username=username,
                            password=password, token=token,
                            availability_zone=availability_zone,
                            region=region)

                if res['NodeList']:
                    for node in res['NodeList']:
                        uuid = uuidutils.generate_uuid()
                        resource_id = res_uuid
                        node_ip = node.get('NodeIP')
                        username = node.get('Username')
                        password = node.get('Password')

                        client.call(ctxt, 'node_create', uuid=uuid,
                                    resource_id=resource_id, node_ip=node_ip,
                                    username=username, password=password)

            return json.dumps(201, {'ContentType': 'application/json'})

    @application.route("/resource/<id>", methods=["GET"])
    def get_resource(id):
        with application.app_context():
            try:
                ctxt = {}
                result = client.call(ctxt, 'resource_detail', id=id)
                return result
            except exceptions.ResourceNotFound:
                msg = "Can not find requested resource: %s" % id
                return exc.HTTPNotFound(explanation=msg)

    @application.route("/resource", methods=["GET"])
    def get_all_resources():
        with application.app_context():
            ctxt = {}
            result = client.call(ctxt, 'get_all_resources')
            return jsonify(result)

    @application.route("/resource/<id>", methods=["DELETE"])
    def resource_delete(id):
        with application.app_context():
            try:
                ctxt = {}
                client.cast(ctxt, 'resource_delete', id=id)
                return {"status": 'success'}, 204
            except exceptions.ResourceNotFound:
                msg = "Can not find requested resource: %s" % id
                return exc.HTTPNotFound(explanation=msg)

    @application.route("/mldata/<id>", methods=["GET"])
    def get_mldata(id):
        with application.app_context():
            try:
                ctxt = {}
                result = client.call(ctxt, 'mldata_detail', id=id)
                return make_response(jsonify(result), 200)
            except exceptions.MLDataNotFound:
                msg = "Can not find requested MLData: %s" % id
                return exc.HTTPNotFound(explanation=msg)

    @application.route("/mldata", methods=["GET"])
    def get_all_mldata():
        with application.app_context():
            ctxt = {}
            result = client.call(ctxt, 'get_all_mldata')
            return jsonify(result)

    @application.route("/mldata/<id>", methods=["DELETE"])
    def mldata_delete(id):
        with application.app_context():
            try:
                ctxt = {}
                client.cast(ctxt, 'mldata_delete', id=id)
                return {"status": 'success'}, 204
            except exceptions.MLDataNotFound:
                msg = "Can not find requested MLData: %s" % id
                return exc.HTTPNotFound(explanation=msg)

    @application.route("/node/<id>", methods=["GET"])
    def get_node(id):
        with application.app_context():
            try:
                ctxt = {}
                result = client.call(ctxt, 'node_detail', id=id)
                return make_response(jsonify(result), 200)
            except exceptions.NodeNotFound:
                msg = "Can not find requested node: %s" % id
                return exc.HTTPNotFound(explanation=msg)

    @application.route("/node", methods=["GET"])
    def get_all_nodes():
        with application.app_context():
            ctxt = {}
            result = client.call(ctxt, 'get_all_nodes')
            return jsonify(result)

    @application.route("/node/<id>", methods=["DELETE"])
    def node_delete(id):
        with application.app_context():
            try:
                ctxt = {}
                client.cast(ctxt, 'node_delete', id=id)
                return {"status": 'success'}, 204
            except exceptions.NodeNotFound:
                msg = "Can not find requested node: %s" % id
                return exc.HTTPNotFound(explanation=msg)
