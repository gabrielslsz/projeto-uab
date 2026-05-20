from app.database import db
from app.models.log_model import LogOperacaoModel
from app.services.job_queue import enfileirar_job


def _persistir_log_operacao(application, usuario_id, acao, tabela_afetada, registro_afetado_id):
    with application.app_context():
        log = LogOperacaoModel(
            usuario_id=usuario_id,
            acao=acao,
            tabela_afetada=tabela_afetada,
            registro_afetado_id=registro_afetado_id,
        )
        db.session.add(log)
        db.session.commit()


def enfileirar_log_operacao(application, usuario_id, acao, tabela_afetada, registro_afetado_id):
    enfileirar_job(
        _persistir_log_operacao,
        application,
        usuario_id,
        acao,
        tabela_afetada,
        registro_afetado_id,
    )