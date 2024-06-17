# import os
# import time
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, jsonify, request
from flask_jwt_extended import  create_access_token

auth = Blueprint('auth', __name__)

users = []


@auth.route("/register",methods=["POST"])
def register():
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"message": "no data provided"})
        username=data["username"]
        password=data["password"]
        for user in users:
            if user['username']==username:
                return jsonify({"message":"user already exist"})
        if username is not None and password is not None:
            hashedPassword=generate_password_hash(password)
            users.append({"username":username,"password":hashedPassword,"role":"user"})
            return jsonify({"message":"user created successfully"})
        return jsonify({"message":"user created successfully"})
    except Exception:
        print(Exception)
        return jsonify("error"), 404

@auth.route('/login', methods=['POST'])
def login():
    data= request.get_json() 
    if data is None:
        return jsonify({"message":"no data provided"})   
    if len(users) == 0:
        return jsonify({"message":"no user is registered"})
    for user in users:
        if user['username'] == data['username'] and check_password_hash(user['password'], data['password']):
            access_token = create_access_token(identity={'username': user['username'] })
            
            return jsonify(access_token)
        else:
            return jsonify({users})
            # return jsonify({"message":"login failed"})