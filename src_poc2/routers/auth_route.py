from fastapi import APIRouter, Depends, Form, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Annotated

from ..schemas.auth_schema import (
    RegisterUser, 
    RegisterUserResponse, 
    Token, 
    LoginUser
)
from ..configurations.database import get_db
from ..services.auth_service import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register", 
    response_model=RegisterUserResponse, 
    description="Register a new user."
)
def register_user(
    user: RegisterUser, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
) -> RegisterUserResponse:
    
    service = AuthService(db)
    return service.create(user, background_tasks)


@router.post(
    "/login", 
    response_model=Token, 
    deprecated=True, 
    description="Login with form data, returns JWT token."
)
def login_user(
    user: Annotated[LoginUser, Form()], 
    db: Session = Depends(get_db)
) -> Token:
    
    service = AuthService(db)
    return service.login_user(user)