from flask_sqlalchemy import SQLAlchemy
from flask import Flask

# Cria a instância do Flask
app = Flask(__name__)

# Configuração do banco MySQL
# Substitua <usuario>, <senha> e <nome_do_banco_de_dados> pelos seus dados
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://biel:novaSenha123@127.0.0.1:3306/auto_nf"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
print("Conectando com URI:", app.config["SQLALCHEMY_DATABASE_URI"])
# Cria a instância do SQLAlchemy
db = SQLAlchemy(app)