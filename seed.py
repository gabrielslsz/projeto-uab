from run import app
from app.database import db
from app.models.models import Sacerdote, Agenda, Atendimento
import os

def seed():
    with app.app_context():
        # Garante que a pasta app/db existe (redundância de segurança)
        db_path = os.path.join(app.root_path, 'db')
        if not os.path.exists(db_path):
            os.makedirs(db_path)
            
        # Cria as tabelas antes de tentar qualquer query
        db.create_all()
        print("Tabelas verificadas/criadas.")

        # Verifica se já existem sacerdotes
        if not Sacerdote.query.first():
            p1 = Sacerdote(nome="Padre Antônio", pin_acesso="123456", status="DISPONIVEL")
            p2 = Sacerdote(nome="Padre José", pin_acesso="654321", status="DISPONIVEL")
            db.session.add_all([p1, p2])
            db.session.commit()
            print("Sacerdotes de teste criados com sucesso!")
        else:
            print("Sacerdotes já existem no banco.")

if __name__ == "__main__":
    seed()
