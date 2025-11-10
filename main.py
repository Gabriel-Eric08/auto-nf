from config_db import app, db 
from models.models import Contrato, Produto, ContratoProduto # <--- ADICIONE ESTA LINHA

from routes.auth import auth_route
from routes.home import home_route
from routes.contratos import contrato_route
from routes.contratoproduto import contrato_produto_route  
from routes.nota_fiscal import nota_fiscal_route
from routes.controlegasto import controle_gasto_route
from routes.notificacoes import notficacoes_route
from routes.relatorios import relatorios_route

# Registra os blueprints
app.register_blueprint(auth_route)
app.register_blueprint(home_route)
app.register_blueprint(contrato_route)
app.register_blueprint(contrato_produto_route )
app.register_blueprint(nota_fiscal_route)
app.register_blueprint(controle_gasto_route)
app.register_blueprint(notficacoes_route)
app.register_blueprint(relatorios_route)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    print("Conectando com URI:", app.config["SQLALCHEMY_DATABASE_URI"])