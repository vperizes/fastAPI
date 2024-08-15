from fastapi import APIRouter, Depends, HTTPException, status
from .. import models, schemas
from sqlalchemy.orm import Session
from ..database import get_db
from ..passwordUtils import verify_password

router = APIRouter(tags=["Authentication"])


@router.post("/login", status_code=status.HTTP_202_ACCEPTED)
def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()


    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    isValidUser = user and verify_password(user_credentials.password, user.password)
    if not isValidUser:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    # where you'd create token
    # return token

    return {"token": 'example token'}
