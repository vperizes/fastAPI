from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from . import models
from .database import engine
from .routes import postRouter, userRouter, authRouter, voteRouter

# comment out create tables since alembic is set up
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()
load_dotenv()

#### CORS setup
origins = ["*"] #setting origin to all domains for testing purposes

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


#### import routes
app.include_router(authRouter.router)
app.include_router(postRouter.router)
app.include_router(userRouter.router)
app.include_router(voteRouter.router)


@app.get("/")
async def root():
    return {"msg": "Welcome"}
