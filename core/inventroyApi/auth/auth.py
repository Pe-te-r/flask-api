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
    role=data['role']
    for user in users:
        if user['username']==username:
            return jsonify({"message":"user already exist"})
    if username is not None and password is not None:
        hashedPassword=generate_password_hash(password)
        users.append({"username":username,"password":hashedPassword,"role":role})
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
            print(payload)
            access_token = jwt.encode(payload, os.getenv("SECRET_KEY"), algorithm="HS256")
            return jsonify(access_token)
        else:
            return jsonify({"message":"login failed"})