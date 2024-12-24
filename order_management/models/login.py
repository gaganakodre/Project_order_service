from datetime import datetime

class Login:
    def __init__(self, user_name, password, email, id=None):
        self.id = id
        self.user_name = user_name
        self.password = password
        self.email = email
        self.created_at = datetime.now()
