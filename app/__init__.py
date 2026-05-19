from flask import Flask, redirect, url_for
from config import Config
from app.database import db

# Import Blueprints
from app.controllers.auth_controller import auth_bp
from app.controllers.proprietario_controller import proprietario_bp
from app.controllers.administrador_controller import admin_bp
from app.controllers.atendente_controller import atendente_bp
from app.controllers.cliente_controller import cliente_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    
    # Registro de Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(proprietario_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(atendente_bp)
    app.register_blueprint(cliente_bp)
    
    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))
    
    return app
