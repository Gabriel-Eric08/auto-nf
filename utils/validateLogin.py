from models.models import User
from flask import request
def validate_login(username, password):
    
    usuario = User.query.filter_by(usuario=username).first()
    if not usuario:
        return False
    elif usuario and usuario.senha == password:
        return True
    else:
        return False

def validate_login_from_cookies():
    # Puxa os valores de 'username' e 'password' dos cookies
    username = request.cookies.get('username')
    password = request.cookies.get('password')

    # Se o username ou a senha não estiverem nos cookies, retorna False
    if not username or not password:
        return False
    
    # Realiza a mesma validação de login
    usuario = User.query.filter_by(usuario=username).first()
    if usuario and usuario.senha == password:
        return True
    else:
        return False