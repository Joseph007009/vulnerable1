"""
SQL Injection Training Lab - Flask Application Factory
EDUCATIONAL USE ONLY
"""
from flask import Flask
from config import config

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Register blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    from admin_panel.routes import admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    from api.endpoints import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app
