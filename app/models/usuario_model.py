from werkzeug.security import check_password_hash, generate_password_hash

from app.database import db


class UsuarioModel(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(
        db.Enum("PROPRIETARIO", "ADMINISTRADOR", "ATENDENTE", "CLIENTE", name="usuario_role"),
        nullable=False,
    )
    criado_por_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=True)

    def set_senha(self, senha_plana):
        self.senha_hash = generate_password_hash(senha_plana)

    def check_senha(self, senha_plana):
        return check_password_hash(self.senha_hash, senha_plana)