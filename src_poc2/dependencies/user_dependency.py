from typing import Annotated
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from .auth_dependency import get_current_user_with_db
from ..schemas.user_schema import UserFullResponse
from ..models.user_model import RoleEnum
from ..exceptions import UnAuthorised


def get_admin_user_with_db(
    user_with_db: Annotated[
        tuple[UserFullResponse, Session], Depends(get_current_user_with_db)
    ]
) -> tuple[UserFullResponse, Session]:
    
    user, db = user_with_db
    if user.role != RoleEnum.admin and user.role != RoleEnum.superadmin:
        raise UnAuthorised()
    return (user, db)


def get_superadmin_user_with_db(
    user_with_db: Annotated[
        tuple[UserFullResponse, Session], Depends(get_current_user_with_db)
    ]
) -> tuple[UserFullResponse, Session]:
    
    user, db = user_with_db
    if user.role != RoleEnum.superadmin:
        raise UnAuthorised()
    return (user, db)
