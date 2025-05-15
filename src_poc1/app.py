from fastapi import FastAPI

from .auth.controller import router as auth_router
from .todos.controller import router as todo_router


todo_app = FastAPI(
    title="Todo Management API",
    version="1.0.0",
    description="""
### ✅ Project Overview

This API provides a comprehensive system for managing personal tasks using FastAPI and SQLAlchemy.

#### 📝 Features

- Create new todos with detailed content
- Retrieve a list of your todos
- View detailed information for each todo
- Update todo content
- Mark todos as complete/incomplete
- Delete todos

#### 🔐 Authentication

All endpoints are secured and require authentication via JWT tokens.

#### 👤 Access Control

- Only the authenticated user can access or modify their own todos.
- No cross-user access is allowed.

""",
    swagger_ui_parameters={"operationsSorter": "method"}
)

todo_app.include_router(todo_router)
todo_app.include_router(auth_router)