from models.models import Registros
from config_db import db

class RegistroRepository:
    def create_registro(self, mensagem, usuario_id, contrato_id):
        novo_registro = Registros(
            mensagem=mensagem,
            usuario_id=usuario_id,
            tabela='contratos',
            id_linha=contrato_id,
            tipo_acao='CREATE',
            alerta=0
        )
        db.session.add(novo_registro)
        db.session.flush()