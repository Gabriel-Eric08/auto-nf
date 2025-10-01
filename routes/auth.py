from flask import Blueprint, render_template, request, jsonify, make_response
from utils.validateLogin import validate_login

auth_route = Blueprint('auth', __name__)

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
        # Cria um objeto de resposta para manipular os cookies
        response = make_response(jsonify({'status': 'success'}), 200)
        # Salva o usuário e a senha nos cookies
        response.set_cookie('username', login)
        response.set_cookie('password', senha)
        return response
    else:
        # Retorna um status de falha no corpo do JSON, também com o código HTTP 200.
        return jsonify({'status': 'failure'}), 200