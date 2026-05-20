from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from app.models.models import Sacerdote, Atendimento
from app.database import db
from app import socketio

sacerdote_bp = Blueprint('sacerdote', __name__)

@sacerdote_bp.route('/sacerdote/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        pin = request.form.get('pin')
        sacerdote = Sacerdote.query.filter_by(pin_acesso=pin).first()
        if sacerdote:
            session['sacerdote_id'] = sacerdote.id
            session['role'] = 'SACERDOTE'
            return redirect(url_for('sacerdote.dashboard'))
        flash("PIN inválido. Tente novamente com calma e oração.")
    return render_template('sacerdote/login.html')

@sacerdote_bp.route('/sacerdote/dashboard')
def dashboard():
    if 'sacerdote_id' not in session:
        return redirect(url_for('sacerdote.login'))
    
    sacerdote = Sacerdote.query.get(session['sacerdote_id'])
    # Fiéis aguardando
    fila = Atendimento.query.filter_by(
        sacerdote_id=sacerdote.id, 
        status='AGUARDANDO'
    ).order_by(Atendimento.criado_em.asc()).all()
    
    # Próximo da fila
    proximo = fila[0] if fila else None
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({
            'total_fila': len(fila),
            'proximo': proximo.identificador_exibicao if proximo else None,
            'fila': [{'id': a.id, 'nome': a.identificador_exibicao, 'hora': a.criado_em.strftime('%H:%M')} for a in fila]
        })
    
    return render_template('sacerdote/dashboard.html', sacerdote=sacerdote, proximo=proximo, total_fila=len(fila))

@sacerdote_bp.route('/sacerdote/chamar-proximo', methods=['POST'])
def chamar_proximo():
    if 'sacerdote_id' not in session:
        return jsonify({"error": "Não autorizado"}), 403
    
    sacerdote_id = session['sacerdote_id']
    proximo = Atendimento.query.filter_by(
        sacerdote_id=sacerdote_id, 
        status='AGUARDANDO'
    ).order_by(Atendimento.criado_em.asc()).first()
    
    if proximo:
        proximo.status = 'CHAMADO'
        db.session.commit()
        
        # Emitir evento para atualizar posição dos fiéis
        socketio.emit('posicao_atualizada', {
            'atendimento_id': proximo.id,
            'sacerdote_id': sacerdote_id
        })
        
        return jsonify({"success": True, "fiel": proximo.identificador_exibicao})
    
    return jsonify({"success": False, "message": "Ninguém na fila"})

@sacerdote_bp.route('/sacerdote/alterar-status', methods=['POST'])
def alterar_status():
    if 'sacerdote_id' not in session:
        return jsonify({"error": "Não autorizado"}), 403
    
    dados = request.get_json()
    novo_status = dados.get('status')
    sacerdote = Sacerdote.query.get(session['sacerdote_id'])
    sacerdote.status = novo_status
    db.session.commit()
    return jsonify({"success": True})

@sacerdote_bp.route('/sacerdote/logout')
def logout():
    session.clear()
    return redirect(url_for('sacerdote.login'))
