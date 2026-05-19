from functools import wraps

from flask import Blueprint, abort, current_app, jsonify, render_template, request, session

from app.services.log_service import enfileirar_log_operacao
from app.services.usuario_service import EmailJaEmUsoError, criar_usuario

admin_bp = Blueprint("administrador", __name__)


def verificar_permissao_admin(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if session.get("user_role") != "ADMINISTRADOR":
            abort(403)
        return view_func(*args, **kwargs)

    return wrapper


@admin_bp.route("/admin/painel")
@verificar_permissao_admin
def painel():
    return render_template("administrador/painel.html")


@admin_bp.route("/admin/atendentes/novo", methods=["POST"])
@verificar_permissao_admin
def criar_atendente():
    dados = request.form
    try:
        novo_atendente = criar_usuario(
            nome=dados.get("nome", ""),
            email=dados.get("email", ""),
            senha=dados.get("senha", ""),
            role="ATENDENTE",
            criado_por_id=session.get("user_id"),
        )
    except EmailJaEmUsoError:
        return jsonify({"error": "Email já em uso"}), 409

    enfileirar_log_operacao(
        current_app._get_current_object(),
        session["user_id"],
        "CRIAR_ATENDENTE",
        "usuarios",
        novo_atendente.id,
    )

    return jsonify({"message": "Atendente criado"}), 201