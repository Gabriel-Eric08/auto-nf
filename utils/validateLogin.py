from models.models import User

def validate_login(username, password):
    
    usuario = User.query.filter_by(usuario=username).first()
    if not usuario:
        return False
    elif usuario and usuario.senha == password:
        return True
    else:
        return False