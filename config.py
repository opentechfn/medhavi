import os


basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(
    basedir, 'sample.sqlite')
transport_url = 'rabbit://neha:admin@192.168.111.133:5672'
rpc_server = '192.168.111.128'
