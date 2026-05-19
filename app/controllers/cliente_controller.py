from flask import Blueprint

cliente_bp = Blueprint("cliente", __name__)


@cliente_bp.route("/cliente/painel")
def painel():
    return "Painel do Cliente"