from repositories.contrato_repository import ContratoRepository
from models.models import ContratoProduto, Produto
from datetime import datetime
from config_db import db


class ContratoService:
    def __init__(self):
        self.repo = ContratoRepository()

    def add_contrato(self, data):
        if not data:
            return False
        
        nome = data.get('nome')
        lotes_ids = data.get('lotes_ids')
        tipo = data.get('tipo')
        
        data_inicial_str = data.get('data_inicial')
        data_final_str = data.get('data_final')

        data_inicial = datetime.strptime(data_inicial_str, '%Y-%m-%d').date()
        data_final = datetime.strptime(data_final_str, '%Y-%m-%d').date()

        if not nome or not lotes_ids or not tipo or not data_final_str or not data_inicial_str:
            return False

        contrato_id = self.repo.create_contrato(nome, tipo, data_inicial, data_final)
        db.session.commit()
        return contrato_id
    
    def existing_contrato(self,nome):
        return self.repo.existing_contrato(nome)
    
    def id_by_nome(self, nome):
        return self.repo.id_by_nome(nome)
    
    def get_all(self):
        return self.repo.get_all()
    
    def lista_produtos(self, contrato_id):
        produtos_do_contrato = db.session.query(ContratoProduto, Produto)\
                                 .join(Produto, ContratoProduto.produto_id == Produto.id)\
                                 .filter(ContratoProduto.contrato_id == contrato_id)\
                                 .all()
        if not produtos_do_contrato:
            return False
        lista_produtos = []
        for cp, produto in produtos_do_contrato:
            lista_produtos.append({
                'id': produto.id,
                'nome': produto.nome,
                'descricao': produto.descricao,
                'preco_unitario': cp.preco_unitario
            })
        return lista_produtos