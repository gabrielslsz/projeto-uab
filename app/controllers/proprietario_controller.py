from flask import Blueprint

proprietario_bp = Blueprint("proprietario", __name__)


@proprietario_bp.route("/proprietario/painel")
def painel():
    return "Painel do Proprietário"