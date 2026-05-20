from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from app.models.models import Sacerdote, Atendimento
from app.services.sacerdote_service import SacerdoteService
from app.services.atendimento_service import AtendimentoService

fiel_bp = Blueprint('fiel', __name__)

@fiel_bp.route('/')
def recepcao():
    sacerdotes = SacerdoteService.get_available_sacerdotes()
    return render_template('fiel/recepcao.html', sacerdotes=sacerdotes)

@fiel_bp.route('/identificacao/<sacerdote_id>')
def identificacao(sacerdote_id):
    sacerdote = SacerdoteService.get_by_id(sacerdote_id)
    if not sacerdote:
        return redirect(url_for('fiel.recepcao'))
    return render_template('fiel/identificacao.html', sacerdote=sacerdote)

@fiel_bp.route('/entrar-fila', methods=['POST'])
def entrar_fila():
    sacerdote_id = request.form.get('sacerdote_id')
    nome_exibicao = request.form.get('nome_exibicao')
    whatsapp = request.form.get('whatsapp')

    atendimento = AtendimentoService.criar_atendimento(sacerdote_id, nome_exibicao, whatsapp)
    return redirect(url_for('fiel.status_atendimento', atendimento_id=atendimento.id))

@fiel_bp.route('/status/<atendimento_id>')
def status_atendimento(atendimento_id):
    atendimento = Atendimento.query.get_or_404(atendimento_id)
    posicao = AtendimentoService.calcular_posicao(atendimento)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({
            'posicao': posicao,
            'status': atendimento.status
        })

    return render_template('fiel/status.html', atendimento=atendimento, posicao=posicao)
