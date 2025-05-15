from sqlalchemy.orm import Session

from ..schemas.user_schema import (
    UserResponse, 
    UserAdminResponse, 
    UserAdminRetrieveResponse,
    UserUpdate
)
from ..repositories.auth_repo import AuthRepository
from ..repositories.user_repo import UserRepository
from ..models.user_model import RoleEnum
from ..exceptions import (
    UserNotFound, 
    UserRoleAlreadyAdmin, 
    UserRoleAlreadyUser
)
from ..utils.user_util import filter_dict


class UserService:

    def __init__(self, db: Session):
        self.auth_repo = AuthRepository(db)
        self.user_repo = UserRepository(db)

    
    def get_users(self, user_role) -> list[UserResponse | UserAdminResponse]:
        if user_role == RoleEnum.admin or user_role == RoleEnum.superadmin:
            return self.user_repo.get_all_users_admins()
        return self.user_repo.get_all_users()


    def get_user_for_admins(self, user_id) -> UserAdminRetrieveResponse:
        user = self.user_repo.get_user_by_id_admins(user_id)
        if not user:
            raise UserNotFound()
        return user
    
    
    def get_user_profile(self, current_user_id):
        user = self.user_repo.get_user_by_id(current_user_id)
        return user
    
    
    def update_user(self, user_id, user_data: UserUpdate) -> UserResponse:
        if not self.user_repo.is_user_exist_by_id(user_id):
            raise UserNotFound()
        user_dict = user_data.model_dump()
        filtered_dict = filter_dict(user_dict)    
        return self.user_repo.update_user_by_id(user_id, filtered_dict)
    
    
    def disable_user(self, user_id):
        if not self.user_repo.get_user_by_id(user_id):
            raise UserNotFound()
        return self.user_repo.disable_user_by_id(user_id)

    
    def enable_user(self, user_id):
        if not self.user_repo.get_user_by_id(user_id):
            raise UserNotFound()
        return self.user_repo.enable_user_by_id(user_id)
    

    def user_to_admin(self, user_role, user_id):
        if not self.user_repo.get_user_by_id(user_id):
            raise UserNotFound()
        if user_role != RoleEnum.user:
            raise UserRoleAlreadyAdmin()
        return self.user_repo.make_user_to_admin(user_id)


    def admin_to_user(self, user_role, user_id):
        if not self.user_repo.get_user_by_id(user_id):
            raise UserNotFound()
        if user_role != RoleEnum.admin:
            raise UserRoleAlreadyUser()
        return self.user_repo.make_admin_to_user(user_id)
    

    def delete_user(self, user_id) -> dict:
        if not self.user_repo.is_user_exist_by_id(user_id):
            raise UserNotFound()
        return self.user_repo.delete_user_by_id(user_id)
