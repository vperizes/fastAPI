from fastapi import FastAPI, status, HTTPException, Response
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import random
import psycopg
from psycopg.rows import dict_row

app = FastAPI()
load_dotenv()


# create schema that extends BaseModel class
class Post(BaseModel):
    title: str
    content: str
    published: bool = True


try:
    conn = psycopg.connect(
        host=os.getenv("HOST"),
        dbname=os.getenv("DBNAME"),
        user=os.getenv("USER"),
        password=os.getenv("PASS"),
        row_factory=dict_row,  # add row factory to return key:val pair
    )

    # Open a cursor to perform database operations
    cur = conn.cursor()
    print("Database connection was successful")
except Exception as err:
    print("Database connection failed")
    print("Error: ", err)


# # temp placeholder in lieu of DB
# my_posts = []


def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post


def find_index_post(id):
    for i, post in enumerate(my_posts):
        if post["id"] == id:
            return i


@app.get("/")
async def root():
    return {"msg": "Welcome"}


@app.get("/posts")
def get_posts():
    cur.execute("SELECT * FROM posts")
    all_posts = cur.fetchall()
    return {"data": all_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cur.execute(
        """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *;""",
        (post.title, post.content, post.published),
    )
    new_post = cur.fetchone()
    conn.commit()  # persist change to db
    return {"data": new_post}


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
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"ID {id} not found"
        )
    my_posts.remove(post)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index == None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"ID {id} not found"
        )
    post_dict = post.model_dump()
    post_dict["id"] = id  # persist id between updates
    my_posts[index] = post_dict
    return {"msg": f"post with ID {id} has been updated", "data": post_dict}
