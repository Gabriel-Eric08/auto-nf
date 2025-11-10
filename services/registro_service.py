from repositories.registro_repository import RegistroRepository
from config_db import db


class RegistroService:
    def __init__(self):
        self.repo = RegistroRepository()
    def create_registro(self,mensagem, usuario_id, contrato_id):
        if not mensagem or not usuario_id or not contrato_id:
            return False
        
        self.repo.create_registro(mensagem, usuario_id, contrato_id)
        db.session.commit()
        return True