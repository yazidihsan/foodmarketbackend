from pydantic_settings import BaseSettings

class MongoSettings(BaseSettings):
    MONGODB_URL: str
    DATABASE_NAME: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = '.env'


# class PostgreSettings(BaseSettings):
#     POSTGRES_USER: str
#     POSTGRES_PASSWORD: str
#     POSTGRES_HOST: str
#     POSTGRES_PORT: int = 5432  # default port
#     POSTGRES_DB: str
#
#     class Config:
#         env_file = '.env'


settings = MongoSettings()
# postgres_settings = PostgreSettings()

