from flask import request
from models.models import User

def get_user_id_from_cookie():
    # 1. Tenta obter o valor do cookie 'username'
    username = request.cookies.get('username')
    
    if not username:
        return None # Usuário não logado ou cookie ausente
        
    # 2. Busca o ID do usuário no banco de dados
    user = User.query.filter_by(usuario=username).first()
    
    if user:
        return user.id
    
    return None # Usuário encontrado