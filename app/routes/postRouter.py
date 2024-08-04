from fastapi import status, HTTPException, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/posts")


###### POST ROUTES ######


@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # cur.execute("SELECT * FROM posts")
    # all_posts = cur.fetchall()
    all_posts = db.query(models.Post).all()
    return all_posts


@router.post("/new", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
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


@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    # cur.execute("""SELECT * FROM posts WHERE id = %s;""", [id])
    # post = cur.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"ID {id} not found"
        )
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
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


@router.put("/{id}", response_model=schemas.Post)
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
