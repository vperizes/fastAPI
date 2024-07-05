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
def get_post(id):
    cur.execute("""SELECT * FROM posts WHERE id = %s;""", [id])
    post = cur.fetchone()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"ID {id} not found"
        )
    return {"post_details": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cur.execute(""" DELETE FROM posts WHERE id = %s RETURNING *; """, [id])
    deleted_post = cur.fetchone()
    conn.commit()
    if not deleted_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"ID {id} not found"
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cur.execute(
        """ UPDATE posts SET title = %s, content = %s, published = %s WHERE id=%s RETURNING *; """,
        (post.title, post.content, post.published, id),
    )
    updated_post = cur.fetchone()
    conn.commit()
    if not updated_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"ID {id} not found"
        )
    return {"msg": f"post with ID {id} has been updated", "data": updated_post}
