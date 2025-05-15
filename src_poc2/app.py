from fastapi import FastAPI

from .routers.user_route import router as user_router
from .routers.auth_route import router as auth_router



auth_app = FastAPI(
    title="User Management API",
    version="1.0.0",
    description="""
### 📘 Project Overview

This API provides a complete system for user registration, authentication, and role-based management using FastAPI and SQLAlchemy.

#### 🔐 Authentication
- Register new users
- Login with JWT-based authentication

#### 👥 User Management
- View and update user profiles
- Admin functionalities to enable/disable users
- Superadmin controls to promote/demote or delete users

#### 🛡 Roles
- **User**: Basic access to their own data
- **Admin**: Manage users
- **Superadmin**: Full access including role control and deletion

""",
    swagger_ui_parameters={"operationsSorter": "method"}
)

auth_app.include_router(user_router)
auth_app.include_router(auth_router)