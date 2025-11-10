from models.models import ContratoProduto

class ContratoRepository:
    def get_all(self):
        return ContratoProduto.query.all()

