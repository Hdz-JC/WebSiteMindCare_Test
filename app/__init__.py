from flask import Flask
from app.controllers.public.main_routes import main_bp


def create_app():
    app = Flask(__name__) 

    app.register_blueprint(main_bp)   
    
    return app
