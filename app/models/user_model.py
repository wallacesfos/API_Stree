from app.configs.database import db
from sqlalchemy import Column, String, Boolean, Integer
from dataclasses import dataclass
from werkzeug.security import generate_password_hash, check_password_hash

@dataclass
class UserModel(db.Model):
    id: int
    email: str
    administer: bool

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(130), nullable=False, unique=True)
    password = Column(String, nullable=False)
    administer = Column(Boolean, default=False)

    @property
    def password_to_hash(self):
        raise AttributeError("Password cannot be accessed!")

    @password_to_hash.setter
    def password_to_hash(self, password):
        self.password = generate_password_hash(password)

    def verify_password(self, password_to_compare):
        return check_password_hash(self.password, password_to_compare)
