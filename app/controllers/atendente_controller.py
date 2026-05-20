from flask import Blueprint, render_template

atendente_bp = Blueprint("atendente", __name__)


@atendente_bp.route("/atendente/painel")
def painel():
    return render_template("atendente/painel.html")