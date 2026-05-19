from flask import Blueprint, request, session, redirect, url_for, flash, jsonify
from app.models.usuario_model import UsuarioModel
from app.database import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    senha = request.form.get('senha')
    usuario = UsuarioModel.query.filter_by(email=email).first()
    
    if usuario and usuario.check_senha(senha):
        session['user_id'] = usuario.id
        session['user_role'] = usuario.role
        return jsonify({"message": f"Bem-vindo {usuario.role}", "role": usuario.role}), 200
    else:
        return jsonify({"error": "Credenciais Inválidas"}), 401

@auth_bp.route('/cadastro-cliente', methods=['POST'])
def cadastro_cliente():
    dados = request.form
    if UsuarioModel.query.filter_by(email=dados.get('email')).first():
        return jsonify({"error": "Email já em uso"}), 400
    
    novo_cliente = UsuarioModel(
        nome=dados.get('nome'),
        email=dados.get('email'),
        role="CLIENTE"
    )
    novo_cliente.set_senha(dados.get('senha'))
    db.session.add(novo_cliente)
    db.session.commit()
    
    return jsonify({"message": "Cliente cadastrado"}), 201
