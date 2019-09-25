from flask_sqlalchemy import SQLAlchemy

from db import model_base as mb


db = SQLAlchemy()


class MLData(db.Model, mb.ModelBase):
    __tablename__ = 'ml_data'
    uuid = db.Column(db.String(36), primary_key=True)
    url = db.Column(db.String(255))
    ml_lib = db.Column(db.String(255))
    is_form_cluster = db.Column(db.Boolean)
    storage_name = db.Column(db.String(255))
    storage_type = db.Column(db.String(255))

    def __init__(self, uuid=None, url=None, ml_lib=None,
                 is_form_cluster=None, storage_name=None,
                 storage_type=None):
        self.uuid = uuid
        self.url = url
        self.ml_lib = ml_lib
        self.is_form_cluster = is_form_cluster
        self.storage_name = storage_name
        self.storage_type = storage_type

    def to_dict(self):
        d = super(MLData, self).to_dict()
        return d


class Resource(db.Model, mb.ModelBase):
    __tablename__ = 'resource'
    uuid = db.Column(db.String(36), primary_key=True)
    resource_type = db.Column(db.String(255))
    provider = db.Column(db.String(255))
    endpoint = db.Column(db.String(255))
    username = db.Column(db.String(30))
    password = db.Column(db.String(30))
    token = db.Column(db.String(255))
    availability_zone = db.Column(db.String(255))
    region = db.Column(db.String(255))
    nodes = db.relationship(
        'Node',
        backref='resource',
        cascade='all, delete, delete-orphan',
        single_parent=True
    )

    def __init__(self, uuid=None, resource_type=None, provider=None,
                 endpoint=None, username=None, password=None, token=None,
                 availability_zone=None, region=None):
        self.uuid = uuid
        self.resource_type = resource_type
        self.provider = provider
        self.endpoint = endpoint
        self.username = username
        self.password = password
        self.token = token
        self.availability_zone = availability_zone
        self.region = region

    def to_dict(self):
        d = super(Resource, self).to_dict()
        d['nodes'] = [r.to_dict() for r in self.nodes]
        return d


class Node(db.Model, mb.ModelBase):
    __tablename__ = 'node'
    uuid = db.Column(db.String(36), primary_key=True)
    resource_id = db.Column(db.String(36), db.ForeignKey('resource.uuid'))
    node_ip = db.Column(db.String(255))
    username = db.Column(db.String(30))
    password = db.Column(db.String(10))

    def __init__(self, uuid=None, resource_id=None, node_ip=None,
                 username=None, password=None):
        self.uuid = uuid
        self.resource_id = resource_id
        self.node_ip = node_ip
        self.username = username
        self.password = password

    def to_dict(self):
        d = super(Node, self).to_dict()
        return d
