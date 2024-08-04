from fastapi import FastAPI
from dotenv import load_dotenv
import os
import psycopg
from psycopg.rows import dict_row

from . import models
from .database import engine
from .routes import postRouter, userRouter

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

#### import routes
app.include_router(postRouter.router)
app.include_router(userRouter.router)


@app.get("/")
async def root():
    return {"msg": "Welcome"}
