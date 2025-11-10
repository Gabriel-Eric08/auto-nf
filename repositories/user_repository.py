from models.models import User

class UserRepository:

    def get_all(self):
        all_users=User.query.all()
    
    def get_id_user_by_username(self, username):
        user = User.query.filter_by(usuario=username).first()
        if not user:
            return False
        return user.id
    
    def get_user_by_name(self, username):
        user = User.query.filter_by(usuario=username).first()
        if not user:
            return False
        return user
    
    def existing_user(self, username, password):
        user=User.query.filter_by(usuario=username, senha=password)
        if not user:
            return False
        return True