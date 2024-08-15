from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def hash(password: str):
    return pwd_context.hash(password)


def authenticate_user(db, username: str, password: str):
    pass
