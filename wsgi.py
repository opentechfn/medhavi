from flask import Flask

application = Flask(__name__)

application.config.from_object('config')

from api.controller import *

if __name__ == '__main__':
    application.run(port=8000)

