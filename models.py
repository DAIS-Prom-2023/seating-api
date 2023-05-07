from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    wxid = Column(String)

    reservations = relationship("Table", back_populates="reserver")


class Table(Base):
    __tablename__ = "tables"

    id = Column(String, primary_key=True, index=True)
    reserved = Column(Boolean, default=False)

    reserver_id = Column(Integer, ForeignKey("users.id"), unique=True)
    reserver = relationship("User", back_populates="reservations")


class Token(Base):
    __tablename__ = "tokens"

    data = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    validated = Column(Boolean, default=False)
