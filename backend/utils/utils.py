from ..dependencies import SessionLocal
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from .user_utils import get_current_user

# Constant defining the maximum allowed size for uploaded content (1MB).
MAX_SIZE = 1_048_576  # 1MB in bytes.

def get_db():
    """
    Dependency function that provides a database session.

    This function acts as a dependency for FastAPI routes. It creates a new SQLAlchemy
    session from the `SessionLocal` factory, yields it to the route function, and ensures
    that the session is closed after the route function completes.

    Returns:
        Session: The SQLAlchemy database session object.
    """
    db = SessionLocal()  # Create a new database session.
    try:
        yield db  # Yield the session to the FastAPI route.
    finally:
        db.close()  # Ensure the session is closed after the route function completes.

# Dependency that will be injected into route functions for database access.
# It uses the `get_db` function to provide the database session to route handlers.
db_dependency = Annotated[Session, Depends(get_db)]  # Annotates the session type.

# Dependency that will be injected into route functions to get the current user.
# It uses the `get_current_user` function to extract the current user from the JWT token.
user_dependency = Annotated[dict, Depends(get_current_user)]  # Annotates the user data type.
