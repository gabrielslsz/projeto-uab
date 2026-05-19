from flask import Blueprint, request, session, abort, jsonify, render_template
from app.models.usuario_model import UsuarioModel
from app.models.ticket_model import TicketModel
from app.models.log_model import LogOperacaoModel
from app.database import db

admin_bp = Blueprint('admin', __name__)

def verificar_permissao_admin():
    if session.get('user_role') != 'ADMINISTRADOR':
        abort(403)

@admin_bp.route('/admin')
def index():
    verificar_permissao_admin()
    return render_template('administrador.html')

@admin_bp.route('/admin/atendentes/novo', methods=['POST'])
def novo_atendente():
    verificar_permissao_admin()
    dados = request.form
    
    novo_atendente = UsuarioModel(
        nome=dados.get('nome'),
        email=dados.get('email'),
        role="ATENDENTE"
    )
    novo_atendente.set_senha(dados.get('senha'))
    db.session.add(novo_atendente)
    db.session.commit()
    
    log = LogOperacaoModel(
        usuario_id=session.get('user_id'),
        acao="CRIAR_ATENDENTE",
        tabela_afetada="usuarios",
        registro_afetado_id=novo_atendente.id
    )
    db.session.add(log)
    db.session.commit()
    
    return jsonify({"message": "Atendente criado"}), 201
