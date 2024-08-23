import bcrypt
from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import Integer, String

from app.database import Base


class User(Base):
    """User database model."""

    __tablename__ = "users"
    __table_args__ = ()

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False, index=True, unique=True)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)

    def __init__(
        self,
        email: str,
        password: str,
        name: str,
    ):
        self.email = email
        self.password = generate_password_hash(password)
        self.name = name.title()

    def check_password(self, password: str) -> bool:
        """Check if the given password is correct."""
        return bcrypt.checkpw(password.encode("ascii"), self.password.encode("ascii"))


def generate_password_hash(password: str) -> str:
    """Bcrypts a password, returns a hash string"""
    pwd_bytes = password.encode("ascii")
    salt_bytes = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt_bytes).decode("ascii")
