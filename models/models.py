# No seu arquivo models.py

from config_db import db
from sqlalchemy.orm import relationship

class Contrato(db.Model):
    __tablename__ = 'contratos'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    casa = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(100), nullable=False)
    
    produtos_do_contrato = db.relationship('ContratoProduto', backref='contrato', lazy=True)
    notas_fiscais = db.relationship('NotaFiscal', backref='contrato', lazy=True)
    
    # Adicionando a relação com ControleGasto
    gastos = db.relationship('ControleGasto', backref='contrato', lazy=True)

    def __repr__(self):
        return f"<Contrato {self.nome}>"

class Produto(db.Model):
    __tablename__ = 'produtos'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(255), nullable=False)
    
    contratos = db.relationship('ContratoProduto', backref='produto', lazy=True)
    
    # Adicionando a relação com ControleGasto
    gastos = db.relationship('ControleGasto', backref='produto', lazy=True)

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

class NotaFiscal(db.Model):
    __tablename__ = 'notas_fiscais'
    
    id = db.Column(db.Integer, primary_key=True)
    
    nome_nf = db.Column(db.Text, nullable=False)
    
    data_emissao = db.Column(db.Date, nullable=False)
    contrato_id = db.Column(db.Integer, db.ForeignKey('contratos.id'), nullable=False)

    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    quantidade_recebida = db.Column(db.Integer, nullable=False)
    preco_unitario_nf = db.Column(db.Float, nullable=False)

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50), nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

class ControleGasto(db.Model):
    __tablename__ = 'controle_gastos'
    id = db.Column(db.Integer, primary_key=True)
    contrato_id = db.Column(db.Integer, db.ForeignKey('contratos.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    gasto_total = db.Column(db.Numeric(precision=10, scale=2), nullable=False, default=0)
    
    quantidade = db.Column(db.Numeric(precision=10, scale=2), nullable=False, default=0)

    def __repr__(self):
        return f"<ControleGasto {self.id}>"