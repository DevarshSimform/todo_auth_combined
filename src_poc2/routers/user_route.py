from fastapi import APIRouter, Depends, Body
from typing import Annotated
from sqlalchemy.orm import Session

from ..schemas.user_schema import (
    UserResponse, 
    UserRetrieveResponse, 
    UserUpdate, 
    DisableUserResponse, 
    UserAdminResponse, 
    UserAdminRetrieveResponse, 
    UserFullResponse
)
from ..services.user_service import UserService
from ..dependencies.auth_dependency import get_current_user_with_db
from ..dependencies.user_dependency import get_admin_user_with_db, get_superadmin_user_with_db


router = APIRouter(
    prefix="/users",
)

get_admin_or_super_admin = Annotated[
    tuple[UserFullResponse, Session], Depends(get_admin_user_with_db)
]


@router.get(
    "/", 
    response_model=list[UserResponse | UserAdminResponse], 
    tags=["Users", "Admin"],
    description="List users (response varies by role)."
)
def get_users(
    user_with_db: tuple[UserFullResponse, Session] = Depends(get_current_user_with_db)
) -> list[UserResponse]:
    
    user, db = user_with_db
    service = UserService(db)
    return service.get_users(user.role)


@router.get(
    "/profile", 
    response_model=UserRetrieveResponse, 
    tags=["Users"],
    description="Get current user's profile."
)
def profile(
    user_with_db: tuple[UserFullResponse, Session] = Depends(get_current_user_with_db)
) -> UserRetrieveResponse:
    
    user, db = user_with_db
    service = UserService(db)
    return service.get_user_profile(user.id)


@router.get(
    "/{user_id}", 
    response_model=UserAdminRetrieveResponse, 
    tags=["Admin"],
    description="Admins fetch specific user details."
)
def get_user(
    user_id: int, 
    user_with_db: tuple[UserFullResponse, Session] = Depends(get_admin_user_with_db)
) -> UserAdminRetrieveResponse:

    user, db = user_with_db
    service = UserService(db)
    return service.get_user_for_admins(user_id)


@router.patch(
    "/", 
    response_model=UserRetrieveResponse, 
    tags=["Users"],
    description="Update current user profile."
)
def update_user(
    user_data: Annotated[UserUpdate, Body()],
    user_with_db: tuple[UserFullResponse, Session] = Depends(get_current_user_with_db)
) -> UserRetrieveResponse:
    
    user, db = user_with_db
    service = UserService(db)
    return service.update_user(user.id, user_data)


@router.patch(
    "/disable", 
    response_model=DisableUserResponse, 
    tags=["Admin"],
    description="Admin disables a user."
)
def disable_user(
    user_id: int, 
    admin_user_with_db: tuple[UserAdminResponse, Session] = Depends(get_admin_user_with_db)
) -> DisableUserResponse:
    
    user, db = admin_user_with_db
    service = UserService(db)
    return service.disable_user(user_id)


@router.patch(
    "/enable", 
    response_model=DisableUserResponse, 
    tags=["Admin"],
    description="Admin enables a user."
)
def enable_user(
    user_id: int, 
    admin_user_with_db: tuple[UserAdminResponse, Session] = Depends(get_admin_user_with_db)
) -> DisableUserResponse:
    
    user, db = admin_user_with_db
    service = UserService(db)
    return service.enable_user(user_id)


@router.patch(
    "/make_admin", 
    response_model=UserAdminRetrieveResponse, 
    tags=["Admin"],
    description="Superadmin promotes user to admin."
)
def make_user_admin(
    user_id: int,
    superadmin_user_with_db: tuple[UserFullResponse, Session] = Depends(get_superadmin_user_with_db)
):
    
    user, db = superadmin_user_with_db
    service = UserService(db)
    return service.user_to_admin(user.role, user_id)


@router.patch(
    "/make_user", 
    response_model=UserAdminRetrieveResponse, 
    tags=["Admin"],
    description="Superadmin demotes admin to user."
)
def make_admin_user(
    user_id: int,
    superadmin_user_with_db: tuple[UserFullResponse, Session] = Depends(get_superadmin_user_with_db)
):
    
    user, db = superadmin_user_with_db
    service = UserService(db)
    return service.admin_to_user(user.role, user_id)


@router.delete(
    "/", 
    tags=["Admin"],
    description="Superadmin deletes a user."
)
def delete_user(
    user_id: int, 
    superadmin_user_with_db: tuple[UserAdminResponse, Session] = Depends(get_superadmin_user_with_db)
):
    
    user, db = superadmin_user_with_db
    service = UserService(db)
    return service.delete_user(user_id)