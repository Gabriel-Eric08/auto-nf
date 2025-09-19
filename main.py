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
    # Este bloco é executado apenas quando o script é rodado diretamente.
    with app.app_context():
        # Antes de recriar/criar, lembre-se de que db.create_all()
        # só adiciona tabelas que não existem. Se a tabela 'contratos'
        # já existia SEM a coluna 'casa', db.create_all() NÃO irá adicioná-la.
        # Por isso, no desenvolvimento, é comum apagar o .db e recriar.
        
        # Opcional: Para garantir que todas as tabelas sejam recriadas do zero
        # se você estiver em fase de desenvolvimento e não se importa com os dados.
        # Comente ou remova esta linha em produção ou quando usar migrações.
        # db.drop_all() 
        
        db.create_all()
        print("Tabelas do banco de dados verificadas/criadas.")

    # Inicia o servidor Flask
    app.run(debug=True, host='0.0.0.0', port=5000)