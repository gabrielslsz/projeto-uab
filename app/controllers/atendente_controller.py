from flask import Blueprint, render_template, session, abort
atendente_bp = Blueprint('atendente', __name__)

@atendente_bp.route('/atendente')
def index():
    if session.get('user_role') != 'ATENDENTE':
        abort(403)
    return render_template('atendente.html')
