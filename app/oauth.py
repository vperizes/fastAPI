from dotenv import load_dotenv
import os
import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta

load_dotenv()

expires_in = os.getenv("JWT_EXPIRES_IN")
secret_key = os.getenv("JWT_SECRET")
algorithm = os.getenv("ALGORITHM")

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now() + expires_delta
    
    else: 
        expire = datetime.now() + timedelta(minutes= int(expires_in))

    to_encode.update({"exp": expire})


    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt