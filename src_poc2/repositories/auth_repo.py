from sqlalchemy.orm import Session
from datetime import datetime

from ..models.user_model import User
from ..schemas.auth_schema import (
    RegisterUser, 
    RegisterUserResponse, 
    LoginUser
)
from ..utils.auth_util import verify_password, get_password_hash


class AuthRepository:
    
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: RegisterUser) -> RegisterUserResponse:
        user = User(
            **data.model_dump(exclude={"password", "confirm_password"}),
            password_hash = get_password_hash(data.password)
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def is_user_exist_in_db(self, email, username):
        return True if self.db.query(User).filter((User.email == email) | (User.username == username)).first() else False
    
    def get_user_by_email(self, email):
        return self.db.query(User).filter_by(email = email).first()
    
    def authenticate_user(self, user_login: LoginUser):
        user = self.db.query(User).filter_by(email = user_login.email).first()
        if not user or not verify_password(user_login.password, user.password_hash):
            return False
        user.last_login = datetime.now()
        self.db.commit()
        return user
    