from common import exceptions
import models
from models import db


def to_dict(func):
    def decorator(*args, **kwargs):
        res = func(*args, **kwargs)
        if isinstance(res, list):
            return [item.to_dict() for item in res]
        if res:
            return res.to_dict()
        else:
            return None
    return decorator


def mldata_create(uuid, url, ml_lib, is_form_cluster, storage_name,
                  storage_type):
    new_mldata = models.MLData(uuid, url, ml_lib, is_form_cluster,
                               storage_name, storage_type)

    db.session.add(new_mldata)
    db.session.commit()


def resource_create(uuid, resource_type, provider, endpoint, username,
                    password, token, availability_zone, region):
    new_res = models.Resource(uuid, resource_type, provider, endpoint,
                              username, password, token,
                              availability_zone, region)
    db.session.add(new_res)
    db.session.commit()


def node_create(uuid, resource_id, node_resource_uuid,
                node_ip, username, password):
    new_node = models.Node(uuid, resource_id, node_ip, username, password)
    new_node_resource = models.NodeResources(node_resource_uuid, uuid)
    db.session.add(new_node)
    db.session.add(new_node_resource)
    db.session.commit()


def add_cpu_details(uuid, node_resource_uuid, model_name, architecture,
                    numa_node_0):
    new_cpu = models.Cpu(uuid, node_resource_uuid, model_name, architecture,
                         numa_node_0)
    db.session.add(new_cpu)
    db.session.commit()


@to_dict
def resource_detail(id=None):
    result = (models.Resource.query.filter(models.Resource.uuid == id)
              .outerjoin(models.Node)
              .one_or_none()
              )

    if result is None:
        raise exceptions.ResourceNotFound(uid=id)

    return result


@to_dict
def node_resource_detail(id=None):
    result = (models.NodeResources.query.filter(
        models.NodeResources.uuid == id)
              .outerjoin(models.Cpu)
              .one_or_none()
              )

    if result is None:
        raise exceptions.NodeResourceNotFound(uid=id)

    return result


@to_dict
def get_all_resources():
    result = models.Resource.query.all()
    return result


@to_dict
def get_all_node_resources():
    result = models.NodeResources.query.all()
    return result


def resource_delete(id=None):
    resource = models.Resource.query.get(id)
    if resource is None:
        return exceptions.ResourceNotFound(uid=id)
    db.session.delete(resource)
    db.session.commit()


@to_dict
def get_all_mldata():
    result = models.MLData.query.all()
    return result


@to_dict
def mldata_detail(id=None):
    result = models.MLData.query.get(id)

    if result is None:
        raise exceptions.MLDataNotFound(uid=id)

    return result


def mldata_delete(id):
    data = models.MLData.query.get(id)
    if data is None:
        raise exceptions.MLDataNotFound(uid=id)

    db.session.delete(data)
    db.session.commit()


@to_dict
def get_all_nodes():
    result = models.Node.query.all()
    return result


@to_dict
def node_detail(id):
    result = models.Node.query.get(id)

    if result is None:
        raise exceptions.NodeNotFound(uid=id)

    return result


def node_delete(id):
    node = models.Node.query.get(id)

    if node is None:
        raise exceptions.NodeNotFound(uid=id)

    db.session.delete(node)
    db.session.commit()
