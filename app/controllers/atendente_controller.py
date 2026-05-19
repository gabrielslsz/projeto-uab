from flask import Blueprint

atendente_bp = Blueprint("atendente", __name__)


@atendente_bp.route("/atendente/painel")
def painel():
    return "Painel do Atendente"