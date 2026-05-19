import pytest
from app.models.usuario_model import UsuarioModel
from app.database import db

def test_login_success(client, app):
    """TC-03: Login com Sucesso"""
    with app.app_context():
        user = UsuarioModel(nome="Admin", email="admin@test.com", role="ADMINISTRADOR")
        user.set_senha("admin123")
        db.session.add(user)
        db.session.commit()

    response = client.post('/login', data={'email': 'admin@test.com', 'senha': 'admin123'})
    # Expecting a redirect or success message based on implementation
    assert response.status_code in [200, 302]

def test_login_invalid_credentials(client):
    """TC-04: Login com Credenciais Inválidas"""
    response = client.post('/login', data={'email': 'wrong@test.com', 'senha': 'wrong'})
    assert response.status_code == 401

def test_cadastro_cliente_duplicate_email(client, app):
    """TC-05: Auto-cadastro de Cliente (Email Único)"""
    with app.app_context():
        user = UsuarioModel(nome="Existente", email="dup@test.com", role="CLIENTE")
        user.set_senha("123")
        db.session.add(user)
        db.session.commit()

    response = client.post('/cadastro-cliente', data={
        'nome': 'Novo',
        'email': 'dup@test.com',
        'senha': '456'
    })
    assert response.status_code == 400
