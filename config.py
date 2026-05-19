import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.getenv("DEBUG_MODE") == "True"
    PROPRIETARIO_EMAIL = os.getenv("PROPRIETARIO_EMAIL")
    PROPRIETARIO_PASSWORD = os.getenv("PROPRIETARIO_PASSWORD")
