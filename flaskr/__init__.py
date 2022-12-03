from flask import Flask
from . import controller

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )
    app.register_blueprint(controller.bp, url_prefix='/api/v1')

    @app.route('/')
    def check():
        return 'The server is running!'

    return app