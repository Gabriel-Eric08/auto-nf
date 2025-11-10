from models.models import ContratoLote
from config_db import db

class ContratoLoteRepository:
    def get_all(self):
        return  ContratoLote.query.all()
    
    def create_association(self, contrato_id, lotes_ids):
        if not contrato_id or not lotes_ids:
            return False
        for lote_id in lotes_ids:
            novo_contrato_lote= ContratoLote(
                contrato_id=contrato_id,
                lote_id=lote_id
            )
            db.session.add(novo_contrato_lote)
        db.session.commit()
        return True
    