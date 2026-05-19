from app import create_app, socketio
from app.database import db
import os

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        # Garante que a pasta app/db existe
        db_path = os.path.join(app.root_path, 'db')
        if not os.path.exists(db_path):
            os.makedirs(db_path)
            print(f"Diretório criado: {db_path}")

        # Importa os modelos para garantir a criação das tabelas
        from app.models.models import Sacerdote, Agenda, Atendimento
        db.create_all()
        print("Ambiente Gratia inicializado com sucesso.")
    
    socketio.run(app, debug=True, host="0.0.0.0", port=5001)
