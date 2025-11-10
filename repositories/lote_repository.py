from models.models import Lote

class LoteRepository:
    def get_all(self):
        lotes = Lote.query.all()
        return lotes