from config_db import app, db 
from models.models import Contrato, Produto, ContratoProduto # <--- ADICIONE ESTA LINHA


# Importa e registra os blueprints
from routes.auth import auth_route
from routes.home import home_route
from routes.contratos import contrato_route
from routes.contratoproduto import contrato_produto_route  
from routes.nota_fiscal import nota_fiscal_route
from routes.controlegasto import controle_gasto_route

# Registra os blueprints
app.register_blueprint(auth_route)
app.register_blueprint(home_route)
app.register_blueprint(contrato_route)
app.register_blueprint(contrato_produto_route )
app.register_blueprint(nota_fiscal_route)
app.register_blueprint(controle_gasto_route)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)