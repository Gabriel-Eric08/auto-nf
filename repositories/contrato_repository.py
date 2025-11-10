from models.models import Contrato
from config_db import db

class ContratoRepository:

    def get_all(self):
        return Contrato.query.all()
    
    def find_by_nome(self, nome):
        return Contrato.query.filter_by(nome=nome).first()
    
    def create_contrato(self, nome, tipo, data_inicial, data_final):
        novo_contrato = Contrato(
            nome=nome,
            tipo=tipo,
            data_inicial=data_inicial,
            data_final=data_final
        )
        db.session.add(novo_contrato)
        db.session.flush()
        return novo_contrato.id

    def delete(self, id):
        contrato = Contrato.query.filter_by(id=id).first()
        if not contrato:
            return False
        db.session.delete(contrato)
        db.session.flush()
        return True
    
    def existing_contrato(self, nome):
        contrato = Contrato.query.filter_by(nome=nome).first()
        if not contrato:
            return False
        return True
    
    def id_by_nome(self,nome):
        contrato = Contrato.query.filter_by(nome=nome).first()
        if not contrato:
            return False
        return contrato.id