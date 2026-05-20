from flask import Flask

from app.database import db
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from app.controllers.administrador_controller import admin_bp
    from app.controllers.atendente_controller import atendente_bp
    from app.controllers.auth_controller import auth_bp
    from app.controllers.cliente_controller import cliente_bp
    from app.controllers.proprietario_controller import proprietario_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(proprietario_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(atendente_bp)
    app.register_blueprint(cliente_bp)

    return app
