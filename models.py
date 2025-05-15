from sqlalchemy import Column, Integer, String
from db import Base

class Product(Base):
    __tablename__ = "produkty"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    quantity = Column(Integer)

class User(Base):  # ✅ DODAJ
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="user")