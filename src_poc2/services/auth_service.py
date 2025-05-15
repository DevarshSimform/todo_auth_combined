from sqlalchemy.orm import Session

from ..schemas.auth_schema import (
    RegisterUser, 
    RegisterUserResponse, 
    LoginUser, 
    Token
)
from ..repositories.auth_repo import AuthRepository
from ..utils.auth_util import create_access_token
from ..utils.user_util import send_welcome_email
from ..exceptions import UserNotFound, UserCreationException



class AuthService:

    def __init__(self, db: Session):
        self.auth_repo = AuthRepository(db)

    def create(self, user: RegisterUser, background_tasks=None) -> RegisterUserResponse:
        if self.auth_repo.is_user_exist_in_db(user.email, user.username):
            raise UserCreationException()
        created_user = self.auth_repo.create(user)
        background_tasks.add_task(send_welcome_email, to_email=created_user.email, data={"username" : f"{created_user.firstname} {created_user.lastname}"})
        return created_user

    def login_user(self, user: LoginUser) -> Token:
        user = self.auth_repo.authenticate_user(user)
        if not user:
            raise UserNotFound()
        access_token = create_access_token(data={"sub": user.email})
        return Token(
            access_token=access_token, token_type="bearer"
        )