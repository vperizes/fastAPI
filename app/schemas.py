from pydantic import BaseModel


# create schema (pydantic model) that extends BaseModel class (defines shape of data)
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
