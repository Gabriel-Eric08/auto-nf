from repositories.contrato__lote_repository import ContratoLoteRepository

class ContratoLoteService:
    def __init__(self):
        self.repo = ContratoLoteRepository()
    
    def create_association(self, contrato_id, lotes_ids):
        if not contrato_id or not lotes_ids:
            return False
        self.repo.create_association(contrato_id, lotes_ids)
        return True