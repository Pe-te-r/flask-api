import os

BASEDIR=os.path.abspath(os.path.dirname(__file__))

class Config():
    SECRET_KEY = os.getenv('SECRET_KEY')
    DEBUG=os.getenv('DEBUG')
    FLASK_ENV=os.getenv('FLASK_ENV')
    FLASK_DEBUG=os.getenv('FLASK_DEBUG')


class DevelopementConfig(Config):
    DEBUG=True


class ProductConfig(Config):
    DEBUG=False