from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


# create schema that extends BaseModel class
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: int | None = None  # setting none makes this field optional


@app.get("/")
async def root():
    return {"msg": "Welcome"}


@app.get("/posts")
def get_posts():
    return {"msg": "here are the posts"}


@app.post("/posts")
# using the body method from fastapi to read the body of the request and assign it to the payload using the spread operator
def new_post(post: Post):
    return post
