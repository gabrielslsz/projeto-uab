from flask import Blueprint, render_template, session, abort
proprietario_bp = Blueprint('proprietario', __name__)

@proprietario_bp.route('/proprietario')
def index():
    if session.get('user_role') != 'PROPRIETARIO':
        abort(403)
    return render_template('proprietario.html')
