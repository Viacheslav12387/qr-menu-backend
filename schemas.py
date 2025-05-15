from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    quantity: int

class UserCreate(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str