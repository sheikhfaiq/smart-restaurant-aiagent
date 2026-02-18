from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.sql import func
import enum
from app.database.session import Base

class RoleEnum(str, enum.Enum):
    ADMIN = "ADMIN"

class User(Base):
    __tablename__ = "User"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.ADMIN)
    createdAt = Column(DateTime(timezone=True), default=func.now())
