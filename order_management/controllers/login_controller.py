from utils.rds_helper import RDSHelper
from models.login import Login
from werkzeug.security import generate_password_hash, check_password_hash

class LoginController:
    def __init__(self):
        self.rds = RDSHelper()

    def create_user(self, user: Login):
        # Hash the password before storing
        user.password = generate_password_hash(user.password)
        sql = """
        INSERT INTO "user" (user_name, password, email, created_at)
        VALUES (%(user_name)s, %(password)s, %(email)s, %(created_at)s)
        RETURNING id;
        """
        _, login_id = self.rds.execute_command_returning_id(sql, vars(user))
        return login_id

    def get_user(self, user_id: int):
        sql = """SELECT * FROM "user" WHERE id = %(user_id)s"""
        result = self.rds.execute_statement(sql, {"user_id": user_id})
        return result[0] if result else None

    def authenticate_user(self, email: str, password: str):
        sql = """SELECT * FROM "user" WHERE email = %(email)s"""
        result = self.rds.execute_statement(sql, {"email": email})
        
        if result and check_password_hash(result[0]['password'], password):
            return result[0]
        return None

    def get_user_by_email(self, email: str):
        sql = """SELECT * FROM "user" WHERE email = %(email)s"""
        result = self.rds.execute_statement(sql, {"email": email})
        return result[0] if result else None
