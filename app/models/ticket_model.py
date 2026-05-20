from datetime import datetime, timezone

from app.database import db


class TicketModel(db.Model):
    __tablename__ = "tickets"

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    assunto = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    status = db.Column(
        db.Enum("ABERTO", "EM_ATENDIMENTO", "RESOLVIDO", name="ticket_status"),
        nullable=False,
        default="ABERTO",
    )
    data_criacao = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    data_atualizacao = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )