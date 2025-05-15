from fastapi import HTTPException, status



class UserException(HTTPException):
    pass


class CredentialException(UserException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Could not validate credentials", 
            headers={"WWW-Authenticate": "Bearer"}
        )

class UserNotFound(UserException):
    def __init__(self, user_id=None):
        message = "User not found" if user_id is None else f"User with id {user_id} not found"
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=message)


class UserCreationException(UserException):
    def __init__(self):
        message = "User already exists with this email"
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=message)


class UserRoleAlreadyAdmin(UserException):
    def __init__(self):
        message = "User Role is already admin"
        super().__init__(status_code=status.HTTP_200_OK, detail=message)


class UserRoleAlreadyUser(UserException):
    def __init__(self):
        message = "User Role is already user"
        super().__init__(status_code=status.HTTP_200_OK, detail=message)


class UnAuthorised(UserException):
    def __init__(self):
        message = "Only Admins and SuperAdmins can access"
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=message)