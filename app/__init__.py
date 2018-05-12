from flask_api import FlaskAPI
from config.config import app_config
from flask import request, jsonify, abort, session
from app.models import Business



def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True) 
    app.secret_key='my-key'
    app.config.from_object(app_config[config_name])

    from .routes import bs as bs_blueprint
    app.register_blueprint(bs_blueprint)

    @app.errorhandler(405)
    def error(error=None):
        return jsonify({"Error":"Wrong access method"})

    
    return app

app = create_app('development')

    
