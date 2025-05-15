from sqlalchemy.orm import Session

from ..models.user_model import User
from ..schemas.user_schema import UserUpdate
from ..models.user_model import RoleEnum


class UserRepository:
    
    def __init__(self, db: Session):
        self.db = db

    
    def is_user_exist_by_id(self, id):
        return True if self.db.query(User).filter_by(id = id, disabled = False).first() else False
    
    def get_all_users(self):
        return self.db.query(
            User.email, User.username, User.firstname, User.lastname, User.bio, User.profile_picture_url, User.last_login
        ).filter_by(disabled = False).all()
    
    def get_all_users_admins(self):
        return self.db.query(User).filter_by(disabled = False).all()
    
    def get_user_by_id(self, id):
        return self.db.query(
            User.id, User.email, User.username, User.firstname, User.lastname, User.bio, User.profile_picture_url, User.last_login, User.created_at, User.updated_at
        ).filter_by(id = id).first()
    
    def get_user_by_id_admins(self, id):
        return self.db.query(User).filter_by(id = id, disabled = False).first()
    
    def get_user_by_username(self, username):
        return self.db.query(User).filter_by(username = username, disabled = False).first()
    
    def disable_user_by_id(self, id):
        db_user = self.db.query(User).filter_by(id = id).first()
        db_user.disabled = True
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def enable_user_by_id(self, id):
        db_user = self.db.query(User).filter_by(id = id).first()
        db_user.disabled = False
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def make_user_to_admin(self, id):
        db_user = self.db.query(User).filter_by(
            id = id, 
        ).first()
        db_user.role = RoleEnum.admin
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def make_admin_to_user(self, id):
        db_user = self.db.query(User).filter_by(
            id = id,
        ).first()
        db_user.role = RoleEnum.admin
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def update_user_by_id(self, id, data: dict):
        db_user = self.db.query(User).filter_by(id = id)
        db_user.update(data)
        self.db.commit()
        return db_user.first()

    def delete_user_by_id(self, id):
        db_user = self.db.query(User).filter_by(id = id)
        db_user.delete()
        self.db.commit()
        return {"detail": "User deleted successfully"}
