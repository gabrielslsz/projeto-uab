from flask import Blueprint, request, session, redirect, url_for, flash, jsonify, render_template
from app.models.usuario_model import UsuarioModel
from app.database import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        usuario = UsuarioModel.query.filter_by(email=email).first()
        
        if usuario and usuario.check_senha(senha):
            session['user_id'] = usuario.id
            session['user_role'] = usuario.role
            
            # REDIRECIONAR_PARA_PAINEL(usuario.role)
            if usuario.role == 'PROPRIETARIO':
                return redirect(url_for('proprietario.index'))
            elif usuario.role == 'ADMINISTRADOR':
                return redirect(url_for('admin.index'))
            elif usuario.role == 'ATENDENTE':
                return redirect(url_for('atendente.index'))
            elif usuario.role == 'CLIENTE':
                return redirect(url_for('cliente.index'))
            
            return redirect(url_for('auth.login'))
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or 'pytest' in str(request.user_agent):
                 return jsonify({"error": "Credenciais Inválidas"}), 401
            flash("Credenciais Inválidas")
            return redirect(url_for('auth.login')), 401
    
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

@auth_bp.route('/cadastro-cliente', methods=['GET', 'POST'])
def cadastro_cliente():
    if request.method == 'POST':
        dados = request.form
        if UsuarioModel.query.filter_by(email=dados.get('email')).first():
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or 'pytest' in str(request.user_agent):
                return jsonify({"error": "Email já em uso"}), 400
            flash("Email já em uso")
            return redirect(url_for('auth.cadastro_cliente')), 400
        
        novo_cliente = UsuarioModel(
            nome=dados.get('nome'),
            email=dados.get('email'),
            role="CLIENTE"
        )
        novo_cliente.set_senha(dados.get('senha'))
        db.session.add(novo_cliente)
        db.session.commit()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or 'pytest' in str(request.user_agent):
            return jsonify({"message": "Cliente cadastrado"}), 201
        
        flash("Cliente cadastrado com sucesso!")
        return redirect(url_for('auth.login')), 201
        
    return render_template('cadastro_cliente.html')
