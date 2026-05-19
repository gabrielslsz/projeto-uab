import os

from dotenv import load_dotenv

load_dotenv()

_basedir = os.path.abspath(os.path.dirname(__file__))


def _as_bool(value):
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "string-aleatoria-segura-aqui")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URI",
        f"sqlite:///{os.path.join(_basedir, 'app', 'db', 'atendimento.db')}",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = _as_bool(os.getenv("DEBUG_MODE", "False"))
    PROPRIETARIO_EMAIL = os.getenv("PROPRIETARIO_EMAIL", "admin@empresa.com")
    PROPRIETARIO_PASSWORD = os.getenv("PROPRIETARIO_PASSWORD", "senha_segura_inicial")
