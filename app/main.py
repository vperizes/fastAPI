from fastapi import FastAPI
from dotenv import load_dotenv
from . import models
from .database import engine
from .routes import postRouter, userRouter, authRouter

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
load_dotenv()

#### import routes
app.include_router(authRouter.router)
app.include_router(postRouter.router)
app.include_router(userRouter.router)


@app.get("/")
async def root():
    return {"msg": "Welcome"}
