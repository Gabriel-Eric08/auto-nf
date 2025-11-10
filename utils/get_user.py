from flask import request
from models.models import User

def get_username_from_cookie():
    # 1. Tenta obter o valor do cookie 'username'
    username = request.cookies.get('username')
    
    if not username:
        return None # Usuário não logado ou cookie ausente
        
    return username