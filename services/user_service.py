from repositories.user_repository import UserRepository

class UserService:
    def __init__(self):
        self.repo=UserRepository()

    def get_id_by_username(self, username):
        return self.repo.get_id_user_by_username(username)
    
    def get_user_by_name(self, username):
        return self.repo.get_user_by_name(username)
    
    def validate_login(self, username, password):
        if not username or not password:
            return True
        if self.repo.existing_user(username, password):
            return True
        return False