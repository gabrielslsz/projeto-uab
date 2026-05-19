from flask import Blueprint, render_template

cliente_bp = Blueprint("cliente", __name__)


@cliente_bp.route("/cliente/painel")
def painel():
    return render_template("cliente/painel.html")