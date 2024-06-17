""" # import os
# import time
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token

auth = Blueprint('auth', __name__)

users = []


@auth.route("/register",methods=["POST"])
def register():
    data = request.get_json()
    if data is None: return jsonify({"message": "no data provided"})
    username=data["username"]
    password=data["password"]
    for user in users:
        if user['username']==username:
            return jsonify({"message":"user already exist"})
    if username != None and password != None:
        hashedPassword=generate_password_hash(password)
        users.append({"username":username,"password":hashedPassword,"role":"user"})
        return jsonify({"message":"user created successfully"})


@auth.route('/login', methods=['POST'])
def login():
    data= request.get_json() 
    if data is None: return jsonify({"message":"no data provided"})   
    if len(users) == 0:return jsonify({"message":"no user is registered"})
    for user in users:
        if user['name'] == data['name'] and check_password_hash(user['password'], data['password']):
            access_token = create_access_token(identity={'username': username})
            
            return jsonify(access_token)
        else:
            return jsonify({"message":"login failed"} }"""

from flask import  Blueprint,request,jsonify
from werkzeug.security import generate_password_hash, check_password_hash
# import time
import datetime
import os
import jwt

auth=Blueprint('auth',__name__)

users=[]


@auth.route("/register",methods=["POST"])
def register():
    data=request.get_json()
    if data is None:
        return jsonify({"message":"no data provided"})
    username=data["username"]
    password=data["password"]
    for user in users:
        if user['username']==username:
            return jsonify({"message":"user already exist"})
    if username is not None and password is not None:
        hashedPassword=generate_password_hash(password)
        users.append({"username":username,"password":hashedPassword,"role":"user"})
        return jsonify({"message":"user created successfully"})


@auth.route('/login', methods=['POST'])
def login():
    data=request.get_json() 
    if data is None:
        return jsonify({"message":"no data provided"})   
    if len(users) == 0:
        return jsonify({"message":"no user is registered"})
    for user in users:
        if user['username']==data['username'] and check_password_hash(user['password'],data['password']):
            payload = {
                "username": user['username'],
                "role": user['role'],
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }
            access_token = jwt.encode(payload, os.getenv("SECRET_KEY"), algorithm="HS256")
            return jsonify(access_token)
        else:
            return jsonify({"message":"login failed"})