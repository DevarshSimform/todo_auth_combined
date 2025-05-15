from enum import Enum as PyEnum
from sqlalchemy import (
    Column, 
    Integer, 
    String,
    Boolean,
    DateTime,
    URL,
    Enum as SQLEnum
)
from zoneinfo import ZoneInfo
from datetime import datetime

from ..configurations.database import Base



class RoleEnum(str, PyEnum):
    user = "user"
    admin = "admin"
    superadmin = "superadmin"


def now_in_timezone():
    return datetime.now(ZoneInfo("Asia/Kolkata"))


class User(Base):

    __tablename__ = "userprofiles"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)

    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    bio = Column(String, nullable=True)
    profile_picture_url = Column(String, nullable=True)

    role = Column(SQLEnum(RoleEnum, name="role_enum"), nullable=False, default=RoleEnum.user)
    disabled = Column(Boolean, default=False, nullable=False)

    created_at = Column(DateTime(timezone=True), default=now_in_timezone)
    updated_at = Column(DateTime(timezone=True), default=None, onupdate=now_in_timezone)
    last_login = Column(DateTime(timezone=True), default=None, onupdate=now_in_timezone)