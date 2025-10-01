from flask import Blueprint, render_template
from utils.validateLogin import validate_login_from_cookies

home_route = Blueprint('home', __name__)

@home_route.route('/home', methods=['GET'])
def home():
    validate = validate_login_from_cookies()
    if validate == True:
        return render_template('home.html')
    else:
        return "Erro de autenticação. Por favor, faça login novamente."