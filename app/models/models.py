from app.database import db
from datetime import datetime
import uuid

class Sacerdote(db.Model):
    __tablename__ = 'sacerdotes'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nome = db.Column(db.String(100), nullable=False)
    pin_acesso = db.Column(db.String(256), nullable=False)
    status = db.Column(db.Enum('DISPONIVEL', 'PAUSADO', 'OFFLINE'), default='OFFLINE')
    agendas = db.relationship('Agenda', backref='sacerdote', lazy=True)

class Agenda(db.Model):
    __tablename__ = 'agendas'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    sacerdote_id = db.Column(db.String(36), db.ForeignKey('sacerdotes.id'), nullable=False)
    dia_semana = db.Column(db.Integer, nullable=False) # 0-6 (Seg-Dom)
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fim = db.Column(db.Time, nullable=False)
    vagas_agendadas = db.Column(db.Integer, default=10)
    permite_fila = db.Column(db.Boolean, default=True)

class Atendimento(db.Model):
    __tablename__ = 'atendimentos'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    identificador_exibicao = db.Column(db.String(50), nullable=False) # Nome ou Código
    telefone = db.Column(db.String(20), nullable=True)
    status = db.Column(db.Enum('AGUARDANDO', 'CHAMADO', 'CONCLUIDO', 'CANCELADO'), default='AGUARDANDO')
    tipo = db.Column(db.Enum('AGENDADO', 'FILA'), default='FILA')
    sacerdote_id = db.Column(db.String(36), db.ForeignKey('sacerdotes.id'), nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
