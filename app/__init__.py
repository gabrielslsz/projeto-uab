from flask import Flask
from config import Config
from app.database import db
from flask_socketio import SocketIO

socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")

    # Registro de Blueprints
    from app.controllers.fiel_controller import fiel_bp
    from app.controllers.sacerdote_controller import sacerdote_bp
    
    app.register_blueprint(fiel_bp)
    app.register_blueprint(sacerdote_bp)

    return app
