from flask import jsonify

from common import exceptions
import models
from models import db


def resource_create(uuid, resource_type, provider, endpoint,
                    username, password, token, availability_zone, region):

    new_res = models.Resource(uuid, resource_type, provider, endpoint,
                              username, password, token, availability_zone,
                              region)

    db.session.add(new_res)
    db.session.commit()


def mldata_create(uuid, url, ml_lib, is_form_cluster,
                  storage_name, storage_type):

    new_mldata = models.MLData(uuid, url, ml_lib, is_form_cluster,
                               storage_name, storage_type)

    db.session.add(new_mldata)
    db.session.commit()


def node_create(uuid, resource_id, node_ip, username, password):
    new_node = models.Node(uuid, resource_id, node_ip, username,
                           password)

    db.session.add(new_node)
    db.session.commit()


def resource_detail(id):
    result = (models.Resource.query.filter(models.Resource.uuid == id)
              .outerjoin(models.Node)
              .one_or_none()
              )
    if result is None:
        raise exceptions.ResourceNotFound(uid=id)

    # Serialize the data for the response
    res_schema = models.ResourceSchema()
    data = res_schema.dump(result).data
    return data


def get_all_resources():
    result = models.Resource.query.all()
    # Serialize the data for the response
    res_schema = models.ResourceSchema(many=True)
    res = res_schema.dump(result)
    return jsonify(res.data)


def resource_delete(id):
    resource = models.Resource.query.get(id)
    if resource is None:
        raise exceptions.ResourceNotFound(uid=id)
    db.session.delete(resource)
    db.session.commit()


def get_all_mldata():
    result = models.MLData.query.all()
    # Serialize the data for the response
    mldata_schema = models.MLDataSchema(many=True)
    res = mldata_schema.dump(result)
    return jsonify(res.data)


def mldata_detail(id):
    result = models.MLData.query.get(id)

    if result is None:
        raise exceptions.MLDataNotFound(uid=id)

    # Serialize the data for the response
    mldata_schema = models.MLDataSchema()
    data = mldata_schema.dump(result).data
    return data


def mldata_delete(id):
    data = models.MLData.query.get(id)
    if data is None:
        raise exceptions.MLDataNotFound(uid=id)

    db.session.delete(data)
    db.session.commit()


def get_all_nodes():
    result = models.Node.query.all()
    # Serialize the data for the response
    node_schema = models.NodeSchema(many=True)
    res = node_schema.dump(result)
    return jsonify(res.data)


def node_detail(id):
    result = models.Node.query.get(id)

    if result is None:
        raise exceptions.NodeNotFound(uid=id)

    # Serialize the data for the response
    node_schema = models.NodeSchema()
    data = node_schema.dump(result).data
    return data


def node_delete(id):
    node = models.Node.query.get(id)

    if node is None:
        raise exceptions.NodeNotFound(uid=id)

    db.session.delete(node)
    db.session.commit()
