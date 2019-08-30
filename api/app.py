import argparse
import json
import os
import sys

from flask import Flask
from flask import request
from flask import jsonify
import mysql.connector as mariadb
from json_parser import JsonParser
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'sample.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    address = db.Column(db.String(120))

    def __init__(self, username=None, email=None, address=None):
        self.username = username
        self.email = email
        self.address = address

@app.route('/user', methods = ['POST'])
def postJsonHandler():
    db.create_all()
    content = request.get_json()
    with open('temp.json', 'w') as f:
        json.dump(content, f)
    json_obj = JsonParser("temp.json")
    username = content['username']
    email = content['email']
    
    new_user = User(username, email)

    db.session.add(new_user)
    db.session.commit()
    json_obj.validate_json_data_type(content)
    json_data = json_obj.parse_json_data()

    return json_data

@app.route("/user/<id>", methods=["GET"])
def user_detail(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)

@app.route("/user", methods=["GET"])
def get_user():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result.data)

@app.route("/user/<id>", methods=["DELETE"])
def user_delete(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return("Delete Sucessfull")

@app.route("/user/<id>", methods=["PUT"])
def user_update(id):
    user = User.query.get(id)
    username = request.json['username']
    email = request.json['email']

    user.email = email
    user.username = username

    db.session.commit()
    return user_schema.jsonify(user)

class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('username', 'email', 'address')


user_schema = UserSchema()
users_schema = UserSchema(many=True)

if __name__ == '__main__':
    app.run(debug=True)
