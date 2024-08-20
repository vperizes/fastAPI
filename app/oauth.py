from dotenv import load_dotenv
import os
import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone
from . import schemas
from fastapi import status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

load_dotenv()

expires_in = os.getenv("JWT_EXPIRES_IN")
secret_key = os.getenv("JWT_SECRET")
algorithm = os.getenv("ALGORITHM")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = 'login')

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    
    else: 
        expire = datetime.now(timezone.utc) + timedelta(minutes= int(expires_in))

    to_encode.update({"exp": expire})


    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, secret_key, algorithms=algorithm)
        id: str = payload.get("users_id")

        if not id:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    
    except InvalidTokenError:
        raise credentials_exception
    
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail = "Could not validate credentials",
        headers = {"WWW-Authenticate": "Bearer"})
    
    return verify_access_token(token, credentials_exception)