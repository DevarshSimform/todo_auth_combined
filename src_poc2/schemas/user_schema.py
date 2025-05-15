from pydantic import BaseModel, EmailStr
from ..models.user_model import RoleEnum
from datetime import datetime


class UserResponse(BaseModel):
    email: EmailStr
    username: str
    firstname: str
    lastname: str
    bio: str | None
    profile_picture_url: str | None


class UserAdminResponse(UserResponse):
    id: int
    role: RoleEnum


class UserFullResponse(UserResponse):
    id: int
    role: RoleEnum
    disabled: bool
    created_at: datetime
    updated_at: datetime | None
    last_login: datetime | None


class UserRetrieveResponse(UserResponse):
    id: int
    created_at: datetime
    updated_at: datetime | None
    last_login: datetime | None


class UserAdminRetrieveResponse(UserRetrieveResponse):
    role: RoleEnum
    disabled: bool


class DisableUserResponse(UserResponse):
    disabled: bool


class UserUpdate(BaseModel):
    firstname: str | None
    lastname: str | None
    bio: str | None
    profile_picture_url: str | None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "firstname": "",
                    "lastname": "",
                    "bio": "",
                    "profile_picture_url": "",
                }
            ]
        }
    }
