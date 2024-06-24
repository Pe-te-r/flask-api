import os
from flask import jsonify, request, Blueprint
from flask_restful import Resource, Api
import jwt


taskBlueprint = Blueprint('taskBlueprint', __name__)
api = Api(taskBlueprint)

tasks=["hello", "world"]

def checkToken(auth_token):
    if not auth_token:
        return jsonify({"message":"unauthorized access"})
    try:
        decoded=jwt.decode(auth_token,os.getenv("SECRET_KEY"),algorithms="HS256")
        print(decoded)
        return decoded
    except jwt.ExpiredSignatureError:
        return jsonify({"message":"token expired"})
    except jwt.InvalidTokenError:
        return jsonify({"message":"invalid token"})
    except jwt.DecodeError:
        return jsonify({"message":"invalid token decode"})

class Task(Resource):
    def get(self, id=None):
        auth_token = request.headers.get("Authorization")
        decoded = checkToken(auth_token)

        if isinstance(decoded, dict):    
            if id is None:
                if decoded['role'] == 'admin':
                    print(decoded['role'])
                    return jsonify(tasks)
                else:
                    return jsonify({"message": "unauthorized access"})
            else:
                try:
                    task_id = int(id)
                    if task_id < len(tasks) and task_id >= 0:
                        return jsonify(tasks[task_id])
                    else:
                        return jsonify({"message": "Task ID out of range."})
                except ValueError:
                    return jsonify({"message": "Invalid task ID format. Please provide an integer."})
                
        return decoded        
    def post(self):
        auth_token = request.headers.get("Authorization")
        decoded=checkToken(auth_token)

        if isinstance(decoded,dict):
            data = request.get_json()
            if data is None:
                return {"message": "No data provided."}, 400


            username=decoded['username']
            info={username: data} 
            tasks.append(info)
            return {"message": "Task created successfully."}, 201
        
        return decoded

api.add_resource(Task,'/task/<int:id>','/task')