# No seu arquivo models.py

from config_db import db
from sqlalchemy.orm import relationship

# Classe de associação para a relação muitos-para-muitos entre Contrato e Lote
class ContratoLote(db.Model):
    __tablename__ = 'contrato_lote'
    
    # As chaves estrangeiras são a chave primária composta
    contrato_id = db.Column(db.Integer, db.ForeignKey('contratos.id'), primary_key=True)
    lote_id = db.Column(db.BigInteger().with_variant(db.Integer, "sqlite"), db.ForeignKey('lotes.id'), primary_key=True)
    
    # Relações bidirecionais
    lote = db.relationship("Lote", back_populates="contratos_associados")
    contrato = db.relationship("Contrato", back_populates="lotes_associados")

    def __repr__(self):
        return f"<ContratoLote ContratoID: {self.contrato_id}, LoteID: {self.lote_id}>"

class Contrato(db.Model):
    __tablename__ = 'contratos'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(100), nullable=False)
    
    # NOVAS COLUNAS DE DATA
    data_inicial = db.Column(db.Date, nullable=False)
    data_final = db.Column(db.Date, nullable=False)
    
    # Adicionando a relação com a tabela de associação ContratoLote
    lotes_associados = db.relationship("ContratoLote", back_populates="contrato", lazy='subquery')

    produtos_do_contrato = db.relationship('ContratoProduto', backref='contrato', lazy=True)
    notas_fiscais = db.relationship('NotaFiscal', backref='contrato', lazy=True)
    gastos = db.relationship('ControleGasto', backref='contrato', lazy=True)

    def __repr__(self):
        return f"<Contrato {self.nome}>"

class Produto(db.Model):
    __tablename__ = 'produtos'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(255), nullable=False)
    
    contratos = db.relationship('ContratoProduto', backref='produto', lazy=True)
    gastos = db.relationship('ControleGasto', backref='produto', lazy=True)

    def __repr__(self):
        return f"<Produto {self.nome}>"

class ContratoProduto(db.Model):
    __tablename__ = 'contrato_produtos'
    
    id = db.Column(db.Integer, primary_key=True)
    contrato_id = db.Column(db.Integer, db.ForeignKey('contratos.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    
    # 💡 NOVO CAMPO: Chave Estrangeira para Lote
    # Assumindo que a quantidade máxima é definida por Contrato, Produto E Lote
    lote_id = db.Column(db.BigInteger().with_variant(db.Integer, "sqlite"), db.ForeignKey('lotes.id'), nullable=False)
    lote = db.relationship('Lote')
    
    quantidade_max = db.Column(db.Integer, nullable=False)
    preco_unitario = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Contrato {self.contrato_id} Produto {self.produto_id} Lote {self.lote_id} Qtd {self.quantidade_max}>"

class RegistroAtividade(db.Model):
    __tablename__ = 'tb_registros'
    
    # Coluna: id (Chave Primária e Auto-incremento)
    id = db.Column(db.Integer, primary_key=True)
    
    # Coluna: usuario (Quem fez a ação)
    # Assumindo que você quer registrar o ID do usuário da tabela 'users'
    usuario_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Coluna: tabela (Qual tabela foi afetada - string)
    tabela = db.Column(db.String(100), nullable=False)
    
    # Coluna: id_linha (ID do registro afetado na tabela original)
    id_linha = db.Column(db.Integer)
    
    # Coluna: data (Quando a ação ocorreu - DATETIME)
    # Usando db.DateTime para incluir a hora
    data = db.Column(db.DateTime, nullable=False, default=db.func.now())
    
    # RELACIONAMENTOS (Opcional, mas recomendado)
    # Cria um relacionamento para buscar o objeto User associado
    usuario = db.relationship('User', backref='registros_atividade')

    def __repr__(self):
        return f"<RegistroAtividade ID: {self.id} UserID: {self.usuario_id} Tabela: {self.tabela}>"

class NotaFiscal(db.Model):
    __tablename__ = 'notas_fiscais'
    
    id = db.Column(db.Integer, primary_key=True)
    nome_nf = db.Column(db.Text, nullable=False)
    data_emissao = db.Column(db.Date, nullable=False)
    
    # Chaves estrangeiras existentes
    contrato_id = db.Column(db.Integer, db.ForeignKey('contratos.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    
    # 💡 NOVO CAMPO: Relacionamento com Lote
    # Usando db.BigInteger() para compatibilidade com o tipo 'id' da classe Lote
    lote_id = db.Column(db.BigInteger, db.ForeignKey('lotes.id'), nullable=False) 
    
    quantidade_recebida = db.Column(db.Integer, nullable=False)
    preco_unitario_nf = db.Column(db.Float, nullable=False)
    
    # Adicione a relação (opcional, mas recomendado)
    lote = db.relationship('Lote') 


class ControleGasto(db.Model):
    __tablename__ = 'controle_gastos'
    id = db.Column(db.Integer, primary_key=True)
    contrato_id = db.Column(db.Integer, db.ForeignKey('contratos.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    
    # 💡 NOVO CAMPO: Chave Estrangeira para Lote
    lote_id = db.Column(db.BigInteger().with_variant(db.Integer, "sqlite"), db.ForeignKey('lotes.id'), nullable=False)
    lote = db.relationship('Lote') 

    gasto_total = db.Column(db.Numeric(precision=10, scale=2), nullable=False, default=0)
    quantidade = db.Column(db.Numeric(precision=10, scale=2), nullable=False, default=0)

    def __repr__(self):
        return f"<ControleGasto {self.id} Contrato: {self.contrato_id} Lote: {self.lote_id}>"
    
class Lote(db.Model):
    __tablename__ = 'lotes'
    
    # id é BIGINT UNSIGNED
    id = db.Column(db.BigInteger().with_variant(db.Integer, "sqlite"), primary_key=True)
    nome_lote = db.Column(db.String(100), nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    casa = db.Column(db.String(100), nullable=False)

    # Adicionando a relação com a tabela de associação ContratoLote
    contratos_associados = db.relationship("ContratoLote", back_populates="lote", lazy='subquery')

    def __repr__(self):
        return f"<Lote {self.nome_lote}>"
    
class ContratoProdutoLote(db.Model):
    __tablename__ = 'contratoproduto_lote'
    
    id = db.Column(db.Integer, primary_key=True)
    contratoproduto_id = db.Column(db.Integer, db.ForeignKey('contrato_produtos.id'), nullable=False)
    lote_id = db.Column(db.BigInteger, db.ForeignKey('lotes.id'), nullable=False)
    
    # Relações
    contrato_produto = db.relationship('ContratoProduto', backref=db.backref('lotes_associados', lazy=True))
    lote = db.relationship('Lote', backref=db.backref('produtos_associados', lazy=True))

    def __repr__(self):
        return f"<ContratoProdutoLote CP_ID:{self.contratoproduto_id} Lote_ID:{self.lote_id}>"

class Registros(db.Model):
    __tablename__ = 'registros'

    id = db.Column(db.Integer, primary_key=True)
    mensagem = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.now()) 
    usuario_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tabela = db.Column(db.String(50), nullable=False)
    id_linha = db.Column(db.Integer, nullable=False)
    tipo_acao = db.Column(db.String(20), nullable=False) 
    alerta = db.Column(db.Integer, nullable=False)


class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50), nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)