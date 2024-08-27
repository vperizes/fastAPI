from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth
from ..database import get_db


router = APIRouter(prefix='/vote', tags=["Votes"])


### user_id will be accessed through token. Req obj should have post id and vote_dir(0=liked, 1=unliked)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.VostCast, current_user: int = Depends(oauth.get_current_user), db: Session = Depends(get_db)):
    pass