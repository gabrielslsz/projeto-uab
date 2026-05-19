from functools import wraps

from flask import Blueprint, abort, jsonify, request, session

from app.database import db
from app.models.log_model import LogOperacaoModel
from app.models.usuario_model import UsuarioModel

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
    return "Painel do Administrador"


@admin_bp.route("/admin/atendentes/novo", methods=["POST"])
@verificar_permissao_admin
def criar_atendente():
    dados = request.form
    email = dados.get("email", "").strip().lower()

    if UsuarioModel.query.filter_by(email=email).first() is not None:
        return jsonify({"error": "Email já em uso"}), 409

    novo_atendente = UsuarioModel(
        nome=dados.get("nome", "").strip(),
        email=email,
        role="ATENDENTE",
        criado_por_id=session.get("user_id"),
    )
    novo_atendente.set_senha(dados.get("senha", ""))

    db.session.add(novo_atendente)
    db.session.flush()

    log = LogOperacaoModel(
        usuario_id=session["user_id"],
        acao="CRIAR_ATENDENTE",
        tabela_afetada="usuarios",
        registro_afetado_id=novo_atendente.id,
    )
    db.session.add(log)
    db.session.commit()

    return jsonify({"message": "Atendente criado"}), 201