# main.py

# Importa as instâncias de 'app' e 'db' do seu arquivo de configuração
from config_db import app, db 

# Importa seus modelos para que db.create_all() os reconheça
# Assumindo que seus modelos estão em um arquivo chamado 'models.py' no mesmo nível
# ou em uma pasta 'models' com um __init__.py
from models.models import Contrato, Produto, ContratoProduto # <--- ADICIONE ESTA LINHA


# Importa e registra os blueprints
from routes.auth import auth_route
from routes.home import home_route
from routes.contratos import contrato_route

# Registra os blueprints
app.register_blueprint(auth_route)
app.register_blueprint(home_route)
app.register_blueprint(contrato_route)

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