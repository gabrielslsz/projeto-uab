from flask import Blueprint, render_template

proprietario_bp = Blueprint("proprietario", __name__)


@proprietario_bp.route("/proprietario/painel")
def painel():
    return render_template("proprietario/painel.html")