from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.models.database import User
from app.models.shemas import UserCreate


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_username(self, username: str):
        return self.db.query(User).filter(User.username == username).first()

    def create(self, user_data: UserCreate):
        db_user = User(
            username=user_data.username,
            hashed_password=get_password_hash(user_data.password),
        )

        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
