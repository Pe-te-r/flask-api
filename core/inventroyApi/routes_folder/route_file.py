from flask import jsonify, request, Blueprint
from flask_restful import Resource, Api
import jwt
from flask_restful import Resource,Api


taskBlueprint = Blueprint('taskBlueprint', __name__)
api = Api(taskBlueprint)

tasks=["hello", "world"]

def checkToken(auth_token):
    if not auth_token:
        return jsonify({"message":"unauthorized access"})
    
    try:
        decoded=jwt.decode(auth_token,'secret_key',algorithms="HS256")
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

        if isinstance(decoded, tuple):  
            return decoded
        
        # Check if ID is provided
        if id is None:
            if decoded['role'] == 'admin':
                return jsonify(tasks)
            else:
                return {"message": "unauthorized access"}, 403
        else:
            # ID is provided, validate the ID
            try:
                task_id = int(id)
            except ValueError:
                return {"message": "Invalid task ID format. Please provide an integer."}, 400
            
            if task_id < 0 or task_id >= len(tasks):
                return {"message": "Task ID out of range."}, 404

            return jsonify(tasks[task_id])
        
    def post(self):
        auth_token = request.headers.get("Authorization")
        decoded = checkToken(auth_token)

        if isinstance(decoded, tuple):  
            return decoded
        
        data = request.get_json()
        if data is None:
            return {"message": "No data provided."}, 400

        if "task" not in data:
            return {"message": "No task provided."}, 400

        tasks.append(data["task"])
        return {"message": "Task created successfully."}, 201


api.add_resource(Task,'/task/<int:id>','/task')