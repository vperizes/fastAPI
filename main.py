from fastapi import FastAPI, status, HTTPException, Response
from pydantic import BaseModel
import random

app = FastAPI()


# create schema that extends BaseModel class
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: int | None = None  # setting none makes this field optional
    id: int = 0


# temp placeholder in lieu of DB
my_posts = []


def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post


@app.get("/")
async def root():
    return {"msg": "Welcome"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def new_post(post: Post):
    post_dict = post.model_dump()  # generate dict rep of model
    post_dict["id"] = random.randint(1, 100000)
    my_posts.insert(0, post_dict)
    return post_dict


@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"ID {id} not found"
        )
    return {"post_details": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"ID {id} not found"
        )
    my_posts.remove(post)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
