from flask_sqlalchemy import SQLAlchemy
from flask import Flask

# Cria a instância do Flask
app = Flask(__name__)

# Configuração do banco SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///controlegastos.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Cria a instância do SQLAlchemy
db = SQLAlchemy(app)
