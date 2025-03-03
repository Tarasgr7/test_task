from fastapi import FastAPI

from .dependencies import Base, engine
from .endpoints.users_endpoints import router as users_router
from.endpoints.posts_endpoints import router as posts_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users_router)
app.include_router(posts_router)