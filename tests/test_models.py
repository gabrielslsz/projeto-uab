import pytest
from app.models.usuario_model import UsuarioModel
from app.database import db

def test_password_hashing(app):
    """TC-01: Criptografia de Senha"""
    with app.app_context():
        user = UsuarioModel(nome="Test User", email="test@example.com", role="CLIENTE")
        user.set_senha("password123")
        db.session.add(user)
        db.session.commit()
        
        assert user.senha_hash != "password123"
        assert user.check_senha("password123") is True
        assert user.check_senha("wrongpassword") is False
