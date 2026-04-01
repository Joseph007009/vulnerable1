"""Secure version of the Flask application - EDUCATIONAL REFERENCE"""
from flask import Flask
from config import config

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    from SECURE_VERSION.app.routes import secure_bp
    app.register_blueprint(secure_bp)
    return app
