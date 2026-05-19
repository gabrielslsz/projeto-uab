from app import create_app
from app.database import db
from app.models.usuario_model import UsuarioModel
from config import Config
import os

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Cria as tabelas se não existirem
        
        # Cria o proprietário inicial se o banco estiver vazio
        if not UsuarioModel.query.filter_by(role="PROPRIETARIO").first():
            novo_proprietario = UsuarioModel(
                email=Config.PROPRIETARIO_EMAIL,
                nome="Proprietário Principal",
                role="PROPRIETARIO"
            )
            novo_proprietario.set_senha(Config.PROPRIETARIO_PASSWORD)
            db.session.add(novo_proprietario)
            db.session.commit()
            print(f"Proprietário inicial criado: {Config.PROPRIETARIO_EMAIL}")
            
    app.run(host="0.0.0.0", port=5000)
