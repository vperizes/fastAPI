from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


############# TOKEN SCHEMAS
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None


############# User schemas
class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True



############# POST SCHEMAS (pydantic models ----> defines shape of data)
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


#### this is response model
class Post(PostBase):
    id: int
    user_id: int
    created_at: datetime
    author: UserOut

    class Config:
        orm_mode = True

############# Vote schemas
class VoteCast(BaseModel):
    post_id: int
    vote_dir: int
