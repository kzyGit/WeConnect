from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from config.config import app_config
from flask import jsonify,Flask, render_template
import logging
import sys
from flask_cors import CORS

db = SQLAlchemy()

def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True) 
    CORS(app)

    app.logger.addHandler(logging.StreamHandler(sys.stdout))
    app.logger.setLevel(logging.ERROR)

    app.secret_key='my-key'
    app.config.from_object(app_config[config_name])

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)#Connect app to the db

    from .routes import bs as bs_blueprint
    app.register_blueprint(bs_blueprint)


    from .routes import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    @app.errorhandler(405)
    def error(error:None):
        return jsonify({"Error":"Wrong access method"}),405

    @app.errorhandler(500)
    def error2(error:None):
        return jsonify({"Error":"No internet connection"}),500
               
    @app.errorhandler(404)
    def error1(error:None):
        return jsonify({"Error":"Invalid access URL"}),404

    return app

app = create_app('development')