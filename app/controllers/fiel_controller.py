from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.models.models import Sacerdote, Atendimento
from app.database import db
from datetime import datetime
from app import socketio

fiel_bp = Blueprint('fiel', __name__)

@fiel_bp.route('/')
def recepcao():
    sacerdotes = Sacerdote.query.filter_by(status='DISPONIVEL').all()
    return render_template('fiel/recepcao.html', sacerdotes=sacerdotes)

@fiel_bp.route('/identificacao/<sacerdote_id>')
def identificacao(sacerdote_id):
    sacerdote = Sacerdote.query.get_or_404(sacerdote_id)
    return render_template('fiel/identificacao.html', sacerdote=sacerdote)

@fiel_bp.route('/entrar-fila', methods=['POST'])
def entrar_fila():
    sacerdote_id = request.form.get('sacerdote_id')
    nome_exibicao = request.form.get('nome_exibicao')
    whatsapp = request.form.get('whatsapp')

    if not nome_exibicao:
        # Gerar código automático se não houver nome
        import random
        nome_exibicao = f"Fiel-{random.randint(100, 999)}"

    novo_atendimento = Atendimento(
        identificador_exibicao=nome_exibicao,
        telefone=whatsapp,
        tipo='FILA',
        sacerdote_id=sacerdote_id,
        status='AGUARDANDO'
    )

    db.session.add(novo_atendimento)
    db.session.commit()

    # Disparar evento SocketIO para o painel do Sacerdote
    socketio.emit('novo_fiel', {
        'sacerdote_id': sacerdote_id,
        'identificador': nome_exibicao
    })

    return redirect(url_for('fiel.status_atendimento', atendimento_id=novo_atendimento.id))

@fiel_bp.route('/status/<atendimento_id>')
def status_atendimento(atendimento_id):
    atendimento = Atendimento.query.get_or_404(atendimento_id)
    # Cálculo simples de posição (exemplo)
    posicao = Atendimento.query.filter(
        Atendimento.sacerdote_id == atendimento.sacerdote_id,
        Atendimento.status == 'AGUARDANDO',
        Atendimento.criado_em < atendimento.criado_em
    ).count() + 1

    return render_template('fiel/status.html', atendimento=atendimento, posicao=posicao)
