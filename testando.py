from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
import os

# Crie seu aplicativo Flask e configure o banco de dados
app = Flask(__name__)
# Usamos um caminho absoluto para evitar problemas de diretório
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'controlecontratos.sqlite3')
db = SQLAlchemy(app)

# Defina seus modelos
class Produto(db.Model):
    __tablename__ = 'produtos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Produto {self.nome}>"

# Este bloco garante que o código seja executado no contexto da aplicação
with app.app_context():
    try:
        # Crie as tabelas do banco de dados, se não existirem
        db.create_all()

        # Agora você pode executar as operações do banco de dados
        p1 = Produto(nome="Caneta")
        p2 = Produto(nome="Lápis")
        
        db.session.add_all([p1, p2])
        db.session.commit()
        
        print("Produtos 'Caneta' e 'Lápis' adicionados com sucesso.")
        print(f"O arquivo do banco de dados está localizado em: {app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')}")
        
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        # Se ocorrer um erro, desfaça as alterações
        db.session.rollback()
    finally:
        # Feche a sessão para garantir que tudo seja gravado no disco
        db.session.close()