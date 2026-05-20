from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from app.services.sacerdote_service import SacerdoteService
from app.services.atendimento_service import AtendimentoService

sacerdote_bp = Blueprint('sacerdote', __name__)

@sacerdote_bp.route('/sacerdote/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        pin = request.form.get('pin')
        sacerdote = SacerdoteService.validate_login(pin)
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
    
    sacerdote_id = session['sacerdote_id']
    sacerdote = SacerdoteService.get_by_id(sacerdote_id)
    fila = AtendimentoService.get_fila_by_sacerdote(sacerdote_id)
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
    
    proximo = AtendimentoService.chamar_proximo(session['sacerdote_id'])
    if proximo:
        return jsonify({"success": True, "fiel": proximo.identificador_exibicao})
    
    return jsonify({"success": False, "message": "Ninguém na fila"})

@sacerdote_bp.route('/sacerdote/alterar-status', methods=['POST'])
def alterar_status():
    if 'sacerdote_id' not in session:
        return jsonify({"error": "Não autorizado"}), 403
    
    dados = request.get_json()
    novo_status = dados.get('status')
    if SacerdoteService.update_status(session['sacerdote_id'], novo_status):
        return jsonify({"success": True})
    return jsonify({"success": False}), 404

@sacerdote_bp.route('/sacerdote/logout')
def logout():
    session.clear()
    return redirect(url_for('sacerdote.login'))
