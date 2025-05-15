import re
from typing import ClassVar
from pydantic import (
    BaseModel, 
    EmailStr, 
    Field, 
    model_validator, 
    field_validator
)

from ..models.user_model import RoleEnum


class RegisterUser(BaseModel):
    username: str
    email: EmailStr
    password: str
    confirm_password: str
    firstname: str
    lastname: str
    bio: str | None
    profile_picture_url: str | None
    role: RoleEnum = RoleEnum.user

    password_regex: ClassVar[str] = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"


    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "devarsh@007",
                    "email": "devarsh@gmail.com",
                    "password": "Admin@123",
                    "confirm_password": "Admin@123",
                    "firstname": "devarsh",
                    "lastname": "chhatrala",
                    "bio": "",
                    "profile_picture_url": "",
                    "role": "user",
                }
            ]
        }
    }


    @model_validator(mode="after")
    def match_passwords(self):
        if self.password != self.confirm_password:
            raise ValueError("Password and Confirm-Password is different")
        return self
    
    @field_validator("password")
    def validate_password(cls, value):
        if not re.fullmatch(cls.password_regex, value):
            raise ValueError("Enter Valid Password")
        return value
    
    


class RegisterUserResponse(BaseModel):
    username: str
    email: EmailStr
    firstname: str
    lastname: str
    bio: str | None
    profile_picture_url: str | None


class LoginUser(BaseModel):
    email: EmailStr = Field(alias="username")
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
