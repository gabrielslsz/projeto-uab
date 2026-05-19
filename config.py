import os
from dotenv import load_dotenv

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "gratia-secret-key-123")
    
    # Busca por GRATIA_DATABASE_URI primeiro para evitar conflito com o projeto anterior
    db_uri = os.getenv("GRATIA_DATABASE_URI")
    if not db_uri:
        # Se não houver, usa o padrão absoluto na pasta app/db
        db_uri = f"sqlite:///{os.path.join(basedir, 'app', 'db', 'gratia.db')}"
    
    SQLALCHEMY_DATABASE_URI = db_uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
