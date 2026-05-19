import pytest
from app.models.usuario_model import UsuarioModel
from app.models.log_model import LogOperacaoModel
from app.database import db

def test_criar_atendente_autorizado(client, app):
    """TC-06: Criação de Atendente (Acesso Autorizado)"""
    with app.app_context():
        admin = UsuarioModel(nome="Admin", email="admin@test.com", role="ADMINISTRADOR")
        admin.set_senha("123")
        db.session.add(admin)
        db.session.commit()
        admin_id = admin.id

    with client.session_transaction() as sess:
        sess['user_id'] = admin_id
        sess['user_role'] = 'ADMINISTRADOR'

    response = client.post('/admin/atendentes/novo', data={
        'nome': 'Atendente 1',
        'email': 'ate1@test.com',
        'senha': '456'
    })
    
    assert response.status_code == 201
    
    with app.app_context():
        atendente = UsuarioModel.query.filter_by(email='ate1@test.com').first()
        assert atendente is not None
        assert atendente.role == 'ATENDENTE'
        
        log = LogOperacaoModel.query.filter_by(acao='CRIAR_ATENDENTE').first()
        assert log is not None
        assert log.usuario_id == admin_id

def test_criar_atendente_negado(client, app):
    """TC-07: Criação de Atendente (Acesso Negado)"""
    with app.app_context():
        cliente = UsuarioModel(nome="Cliente", email="cli@test.com", role="CLIENTE")
        cliente.set_senha("123")
        db.session.add(cliente)
        db.session.commit()
        cliente_id = cliente.id

    with client.session_transaction() as sess:
        sess['user_id'] = cliente_id
        sess['user_role'] = 'CLIENTE'

    response = client.post('/admin/atendentes/novo', data={
        'nome': 'Atendente Fake',
        'email': 'fake@test.com',
        'senha': '456'
    })
    
    assert response.status_code == 403
