from oslo_config import cfg
import oslo_messaging as om

import config
from common import exceptions
from migrate import app
import models
from models import db


# Invoke "get_transport". This call will set default Configurations required
# to Create Messaging Transport
transport = om.get_transport(cfg.CONF)

# Set/Override Configurations required to Create Messaging Transport
cfg.CONF.set_override('transport_url', config.transport_url)

# Create Messaging Transport
transport = om.get_transport(cfg.CONF)

# Create Target (Exchange, Topic and Server to listen on)
target = om.Target(topic='testme', server=config.rpc_server)


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


# Create EndPoint
class TestEndpoint(object):

    def mldata_create(self, ctxt=None, uuid=None, url=None, ml_lib=None,
                      is_form_cluster=None, storage_name=None,
                      storage_type=None):
        with app.app_context():
            new_mldata = models.MLData(uuid, url, ml_lib, is_form_cluster,
                                       storage_name, storage_type)

            db.session.add(new_mldata)
            db.session.commit()

    def resource_create(self, ctxt=None, uuid=None, resource_type=None,
                        provider=None, endpoint=None,
                        username=None, password=None, token=None,
                        availability_zone=None, region=None):
        with app.app_context():
            new_res = models.Resource(uuid, resource_type, provider, endpoint,
                                      username, password, token,
                                      availability_zone, region)

            db.session.add(new_res)
            db.session.commit()

    def node_create(self, ctxt=None, uuid=None, resource_id=None,
                    node_ip=None, username=None, password=None):
        with app.app_context():
            new_node = models.Node(uuid, resource_id, node_ip, username,
                                   password)

            db.session.add(new_node)
            db.session.commit()

    @to_dict
    def resource_detail(self, ctxt=None, id=None):
        with app.app_context():
            result = (models.Resource.query.filter(models.Resource.uuid == id)
                      .outerjoin(models.Node)
                      .one_or_none()
                      )

            if result is None:
                raise exceptions.ResourceNotFound(uid=id)

            return result

    @to_dict
    def get_all_resources(self, ctxt=None):
        with app.app_context():
            result = models.Resource.query.all()
            return result

    def resource_delete(self, ctxt=None, id=None):
        with app.app_context():
            resource = models.Resource.query.get(id)
            if resource is None:
                return exceptions.ResourceNotFound(uid=id)
            db.session.delete(resource)
            db.session.commit()

    @to_dict
    def get_all_mldata(self, ctxt=None):
        with app.app_context():
            result = models.MLData.query.all()
            return result

    @to_dict
    def mldata_detail(self, ctxt=None, id=None):
        with app.app_context():
            result = models.MLData.query.get(id)

            if result is None:
                raise exceptions.MLDataNotFound(uid=id)

            return result

    def mldata_delete(self, ctxt=None, id=None):
        with app.app_context():
            data = models.MLData.query.get(id)
            if data is None:
                raise exceptions.MLDataNotFound(uid=id)

            db.session.delete(data)
            db.session.commit()

    @to_dict
    def get_all_nodes(self, ctxt=None):
        with app.app_context():
            result = models.Node.query.all()
            return result

    @to_dict
    def node_detail(self, ctxt=None, id=None):
        with app.app_context():
            result = models.Node.query.get(id)

            if result is None:
                raise exceptions.NodeNotFound(uid=id)

            return result

    def node_delete(self, ctxt=None, id=None):
        with app.app_context():
            node = models.Node.query.get(id)

            if node is None:
                raise exceptions.NodeNotFound(uid=id)

            db.session.delete(node)
            db.session.commit()


# Create EndPoint List
endpoints = [TestEndpoint(), ]

# Create RPC Server
server = om.get_rpc_server(transport, target, endpoints)

# Start RPC Server
server.start()
