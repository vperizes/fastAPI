from fastapi import FastAPI, status, HTTPException, Response, Depends
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os
import psycopg
from psycopg.rows import dict_row
from typing import List

from . import models, schemas
from .database import engine, get_db
from .passwordUtils import get_password

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
load_dotenv()

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


###### USER ROUTES ######
@app.post(
    "/new-user", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut
)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # hash password - user.password
    hashed_password = get_password(user.password)
    user.password = hashed_password

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/users/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id: {id} not found.",
        )
    return user


###### POST ROUTES ######


@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # cur.execute("SELECT * FROM posts")
    # all_posts = cur.fetchall()
    all_posts = db.query(models.Post).all()
    return all_posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cur.execute(
    #     """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *;""",
    #     (post.title, post.content, post.published),
    # )
    # new_post = cur.fetchone()
    # conn.commit()  # persist change to db

    # **post.model_dump() creates a dict and unpacks it with "**". This replaces the need for 'title=post.title, ...'

    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    # cur.execute("""SELECT * FROM posts WHERE id = %s;""", [id])
    # post = cur.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"ID {id} not found"
        )
    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cur.execute(""" DELETE FROM posts WHERE id = %s RETURNING *; """, [id])
    # deleted_post = cur.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"ID {id} not found"
        )

    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cur.execute(
    #     """ UPDATE posts SET title = %s, content = %s, published = %s WHERE id=%s RETURNING *; """,
    #     (post.title, post.content, post.published, id),
    # )
    # updated_post = cur.fetchone()
    # conn.commit()
    updated_post = db.query(models.Post).filter(models.Post.id == id)

    if not updated_post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"ID {id} not found"
        )

    updated_post.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return {"msg": f"post with ID {id} has been updated", "data": updated_post.first()}
