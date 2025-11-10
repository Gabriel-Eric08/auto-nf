from repositories.lote_repository import LoteRepository

class LoteService:
    def __init__(self):
        self.repo = LoteRepository()

    def get_all(self):
        return self.repo.get_all()