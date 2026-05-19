import os

from app import create_app
from app.database import db
from app.services.usuario_service import garantir_proprietario_inicial

app = create_app()


def ensure_database_directory(application):
    if application.config["SQLALCHEMY_DATABASE_URI"].startswith("sqlite:///"):
        database_path = application.config["SQLALCHEMY_DATABASE_URI"].replace("sqlite:///", "", 1)
        directory = os.path.dirname(database_path)
        if directory:
            os.makedirs(directory, exist_ok=True)


def initialize_database(application):
    ensure_database_directory(application)
    with application.app_context():
        db.create_all()
        garantir_proprietario_inicial(application)


if __name__ == "__main__":
    initialize_database(app)
    app.run(host="0.0.0.0", port=5000, debug=app.config["DEBUG"])
