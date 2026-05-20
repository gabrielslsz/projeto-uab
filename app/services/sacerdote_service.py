from app.models.models import Sacerdote
from app.database import db
from app.services.cache_service import CacheService

class SacerdoteService:
    CACHE_KEY_AVAILABLE = "sacerdotes_disponiveis"

    @staticmethod
    def get_available_sacerdotes():
        cached = CacheService.get(SacerdoteService.CACHE_KEY_AVAILABLE)
        if cached is not None:
            return cached
        
        sacerdotes = Sacerdote.query.filter_by(status='DISPONIVEL').all()
        CacheService.set(SacerdoteService.CACHE_KEY_AVAILABLE, sacerdotes, timeout=300)
        return sacerdotes

    @staticmethod
    def get_by_id(sacerdote_id):
        return Sacerdote.query.get(sacerdote_id)

    @staticmethod
    def validate_login(pin):
        return Sacerdote.query.filter_by(pin_acesso=pin).first()

    @staticmethod
    def update_status(sacerdote_id, novo_status):
        sacerdote = Sacerdote.query.get(sacerdote_id)
        if sacerdote:
            sacerdote.status = novo_status
            db.session.commit()
            CacheService.delete(SacerdoteService.CACHE_KEY_AVAILABLE)
            return True
        return False
