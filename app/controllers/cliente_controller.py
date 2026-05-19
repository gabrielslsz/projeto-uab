from flask import Blueprint, render_template, session, abort
cliente_bp = Blueprint('cliente', __name__)

@cliente_bp.route('/cliente')
def index():
    if session.get('user_role') != 'CLIENTE':
        abort(403)
    return render_template('cliente.html')
