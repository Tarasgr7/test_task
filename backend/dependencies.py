import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base,Session
from fastapi import Depends
from dotenv import load_dotenv
from typing import Annotated

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")


DATABASE_URL = os.getenv("DB_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()



from .models.post_model import PostModel
from .models.users_model import UserModel



