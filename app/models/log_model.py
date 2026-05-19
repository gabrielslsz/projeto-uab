from app.database import db
from datetime import datetime

class LogOperacaoModel(db.Model):
    __tablename__ = "logs_operacoes"
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    acao = db.Column(db.String(100), nullable=False)
    tabela_afetada = db.Column(db.String(100), nullable=False)
    registro_afetado_id = db.Column(db.Integer, nullable=False)
    data_hora = db.Column(db.DateTime, default=datetime.utcnow)
