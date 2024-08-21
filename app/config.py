from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_hostname: str
    db_port: str
    db_name: str
    db_username: str
    db_password: str
    jwt_secret: str
    algorithm: str
    jwt_expires_in_minutes: int

    class Config:
        env_file= ".env"


settings = Settings()
