from flask import Blueprint, abort, redirect, request, session, url_for

from app.database import db
from app.models.usuario_model import UsuarioModel

auth_bp = Blueprint("auth", __name__)


ROLE_ENDPOINTS = {
    "PROPRIETARIO": "proprietario.painel",
    "ADMINISTRADOR": "administrador.painel",
    "ATENDENTE": "atendente.painel",
    "CLIENTE": "cliente.painel",
}


@auth_bp.route("/login", methods=["POST"])
def login():
    email = request.form.get("email", "").strip().lower()
    senha = request.form.get("senha", "")

    usuario = UsuarioModel.query.filter_by(email=email).first()
    if usuario is None or not usuario.check_senha(senha):
        return "Credenciais Inválidas", 401

    session["user_id"] = usuario.id
    session["user_role"] = usuario.role
    endpoint = ROLE_ENDPOINTS.get(usuario.role)
    if endpoint is None:
        abort(403)
    return redirect(url_for(endpoint))


@auth_bp.route("/cadastro-cliente", methods=["POST"])
def cadastro_cliente():
    dados = request.form
    email = dados.get("email", "").strip().lower()

    if UsuarioModel.query.filter_by(email=email).first() is not None:
        return "Email já em uso", 409

    novo_cliente = UsuarioModel(
        nome=dados.get("nome", "").strip(),
        email=email,
        role="CLIENTE",
    )
    novo_cliente.set_senha(dados.get("senha", ""))

    db.session.add(novo_cliente)
    db.session.commit()

    return "Cliente cadastrado", 201