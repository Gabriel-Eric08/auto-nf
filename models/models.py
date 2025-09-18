from config_db import db

class Contrato(db.Model):
    __tablename__ = 'contratos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    casa = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(100), nullable=False)
    # relacionamento com os itens do contrato
    produtos_do_contrato = db.relationship('ContratoProduto', backref='contrato', lazy=True)

    def __repr__(self):
        return f"<Contrato {self.nome}>"

class Produto(db.Model):
    __tablename__ = 'produtos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(255), nullable=False)
    
    # Adicionando um relacionamento de volta para a tabela de junção
    contratos = db.relationship('ContratoProduto', backref='produto', lazy=True)

    def __repr__(self):
        return f"<Produto {self.nome}>"

class ContratoProduto(db.Model):
    __tablename__ = 'contrato_produtos'
    id = db.Column(db.Integer, primary_key=True)
    contrato_id = db.Column(db.Integer, db.ForeignKey('contratos.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    quantidade_max = db.Column(db.Integer, nullable=False)
    preco_unitario = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Contrato {self.contrato_id} Produto {self.produto_id} Qtd {self.quantidade_max}>"