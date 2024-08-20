from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import models, schemas, oauth
from sqlalchemy.orm import Session
from ..database import get_db
from ..passwordUtils import verify_password

router = APIRouter(tags=["Authentication"])


@router.post("/login", status_code=status.HTTP_202_ACCEPTED)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()


    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    isValidUser = user and verify_password(user_credentials.password, user.password)
    if not isValidUser:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    
    access_token = oauth.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
