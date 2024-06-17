from flask import Response, Blueprint,request,jsonify
import jwt
import time
import os

auth=Blueprint('auth',__name__)

users=[]


@auth.route("/register",methods=["POST"])
def register():
    data=request.get_json()
    for user in users:
        if user['name'] == data['name']:
            return jsonify({"message":"user already exist"})
    if data['name'] != None and data['password'] != None:
        users.append(data)
        return jsonify({"message":"user created successfully"})
    else:
        return jsonify({"message":"name and password are required"})

@auth.route('/login', methods=['POST'])
def login():
    data=request.get_json() 
    if data is None: return jsonify({"message":"no data provided"})   
    if len(users) == 0: return jsonify({"message":"no user is registered"})
    for user in users:
        if user['name']==data['name'] and user['password']==data['password']:
            data={
                "name":data['name'],
                "role":user['role'],
                "exp": int(time.time() + 60 * 60) 
            }

            token = jwt.encode(data, "secret_key", algorithm="HS256")
            response_data={
                "message":"login successfull",
                "token":{"token":token}
            }
            return jsonify(response_data)
        else:
            return jsonify({"message":"login failed"})