from datetime import datetime, timezone

from app.database import db


class LogOperacaoModel(db.Model):
    __tablename__ = "logs_operacoes"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    acao = db.Column(db.String(120), nullable=False)
    tabela_afetada = db.Column(db.String(120), nullable=False)
    registro_afetado_id = db.Column(db.Integer, nullable=False)
    data_hora = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))