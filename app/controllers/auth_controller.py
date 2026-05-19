from flask import Blueprint, abort, redirect, request, session, url_for

from app.services.usuario_service import autenticar_usuario, criar_usuario, EmailJaEmUsoError

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

    usuario = autenticar_usuario(email, senha)
    if usuario is None:
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
    try:
        criar_usuario(
            nome=dados.get("nome", ""),
            email=dados.get("email", ""),
            senha=dados.get("senha", ""),
            role="CLIENTE",
        )
    except EmailJaEmUsoError:
        return "Email já em uso", 409

    return "Cliente cadastrado", 201