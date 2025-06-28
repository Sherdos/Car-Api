



from src.apps.user.repositories import UserRepository


class UserService:
    def __init__(self, db_session):
        self.db_session = db_session
        self.repository = UserRepository(db_session)

    def create_user(self, user):
        new_user = self.repository.create_user(user)
        return new_user

    def get_user_by_id(self, user_id):
        return self.repository.get_user_by_id(user_id)

    def get_user_by_username(self, username):
        return self.repository.get_user_by_username(username)
    
    def get_user_by_email(self, email): 
        return self.repository.get_user_by_email(email)
    
    def update_user(self, user_id, user:):
        old_user = self.repository.get_user_by_id(user_id)
        
        updated_user = self.repository.update_user(user)
        return updated_user