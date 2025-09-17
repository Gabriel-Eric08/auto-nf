from flask import Blueprint, render_template, request
from utils.validateLogin import validate_login

auth_route = Blueprint('auth', __name__ )

@auth_route.route('/')
def login_page():
    return render_template('login_page.html')

@auth_route.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    login = data.get('login')
    senha = data.get('senha')

    # A variável 'is_valid_login' evita o conflito de nomes
    is_valid_login = validate_login(login, senha)
    
    if is_valid_login:
        # Retorna um status de sucesso no corpo do JSON, com o código HTTP 200.
        return {'status': 'success'}, 200 
    else:
        # Retorna um status de falha no corpo do JSON, também com o código HTTP 200.
        return {'status': 'failure'}, 200