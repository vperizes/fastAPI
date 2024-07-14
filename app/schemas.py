from pydantic import BaseModel
from datetime import datetime


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
