import os

from app import create_app
from app.database import db
from app.models import UsuarioModel

app = create_app()


def ensure_database_directory(application):
    if application.config["SQLALCHEMY_DATABASE_URI"].startswith("sqlite:///"):
        database_path = application.config["SQLALCHEMY_DATABASE_URI"].replace("sqlite:///", "", 1)
        directory = os.path.dirname(database_path)
        if directory:
            os.makedirs(directory, exist_ok=True)


def seed_initial_owner(application):
    existing_owner = UsuarioModel.query.filter_by(email=application.config["PROPRIETARIO_EMAIL"]).first()
    if existing_owner is None:
        owner = UsuarioModel(
            nome="Proprietário Principal",
            email=application.config["PROPRIETARIO_EMAIL"],
            role="PROPRIETARIO",
        )
        owner.set_senha(application.config["PROPRIETARIO_PASSWORD"])
        db.session.add(owner)
        db.session.commit()


def initialize_database(application):
    ensure_database_directory(application)
    with application.app_context():
        db.create_all()
        seed_initial_owner(application)


if __name__ == "__main__":
    initialize_database(app)
    app.run(host="0.0.0.0", port=5000, debug=app.config["DEBUG"])
