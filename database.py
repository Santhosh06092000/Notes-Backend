from sqlalchemy import create_engine

from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_URL: str


settings = Settings()

print("check", settings.DB_URL)

DATABASE_URL = settings.DB_URL

engine = create_engine(DATABASE_URL)


# create db and tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# session dependancy


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
