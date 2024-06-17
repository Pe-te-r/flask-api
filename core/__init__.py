import os
from flask import  Flask
from dotenv import load_dotenv

from .inventroyApi import auth
from .inventroyApi import taskBlueprint


load_dotenv()

print("hello people!")

def create_app(config_type=os.getenv("CONFIG_TYPE")):
    app = Flask(__name__)
    app.register_blueprint(taskBlueprint,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')
    app.config.from_object(config_type)
    
    return app