from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class User(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True


# create schema (pydantic model) that extends BaseModel class (defines shape of data)
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


#### this is response model
class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
