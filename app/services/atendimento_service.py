from app.models.models import Atendimento
from app.database import db
from app import socketio

class AtendimentoService:
    @staticmethod
    def criar_atendimento(sacerdote_id, identificador, telefone=None):
        if not identificador:
            import random
            identificador = f"Fiel-{random.randint(100, 999)}"

        novo = Atendimento(
            identificador_exibicao=identificador,
            telefone=telefone,
            tipo='FILA',
            sacerdote_id=sacerdote_id,
            status='AGUARDANDO'
        )
        db.session.add(novo)
        db.session.commit()

        # Emitir evento SocketIO
        socketio.emit('novo_fiel', {
            'sacerdote_id': sacerdote_id,
            'identificador': identificador
        })
        return novo

    @staticmethod
    def get_fila_by_sacerdote(sacerdote_id):
        return Atendimento.query.filter_by(
            sacerdote_id=sacerdote_id, 
            status='AGUARDANDO'
        ).order_by(Atendimento.criado_em.asc()).all()

    @staticmethod
    def chamar_proximo(sacerdote_id):
        proximo = Atendimento.query.filter_by(
            sacerdote_id=sacerdote_id, 
            status='AGUARDANDO'
        ).order_by(Atendimento.criado_em.asc()).first()
        
        if proximo:
            proximo.status = 'CHAMADO'
            db.session.commit()
            
            socketio.emit('posicao_atualizada', {
                'atendimento_id': proximo.id,
                'sacerdote_id': sacerdote_id
            })
            return proximo
        return None

    @staticmethod
    def calcular_posicao(atendimento):
        if atendimento.status == 'CHAMADO':
            return 0
        if atendimento.status in ['CONCLUIDO', 'CANCELADO']:
            return -1
            
        return Atendimento.query.filter(
            Atendimento.sacerdote_id == atendimento.sacerdote_id,
            Atendimento.status == 'AGUARDANDO',
            Atendimento.criado_em < atendimento.criado_em
        ).count() + 1
