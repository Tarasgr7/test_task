from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from ..models.users_model import UserModel
from typing import Annotated 
from ..dependencies import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# OAuth2 password bearer used for token authentication.
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/token')

# Password context for hashing and verifying passwords using bcrypt.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    """
    Verifies a plain password against a hashed password.

    Args:
        plain_password (str): The plain password to verify.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the plain password matches the hashed password, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password):
    """
    Hashes a plain password using bcrypt.

    Args:
        password (str): The plain password to hash.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)


def authenticate_user(email: str, password: str, db):
    """
    Authenticates a user by verifying their email and password.

    Args:
        email (str): The user's email.
        password (str): The plain password to verify.
        db (SQLAlchemy Session): The database session to query the UserModel.

    Returns:
        UserModel | False: The user object if authentication is successful, False if unsuccessful.
    """
    user = db.query(UserModel).filter(UserModel.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        return False  # Authentication failed.
    return user  # Authentication successful.


def create_access_token(email: str, id: int, expires_delta: timedelta = None):
    """
    Creates a JWT access token with the provided email, user ID, and expiration time.

    Args:
        email (str): The user's email (used as the 'sub' claim in the token).
        id (int): The user's ID.
        expires_delta (timedelta, optional): The time duration after which the token will expire.
        
    Returns:
        str: The JWT access token as a string.
    """
    to_encode = {
        "sub": email,  # Subject claim (the user's email).
        "id": id,      # Custom claim for the user's ID.
    }
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})  # Expiration claim.
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # Encode the token.



async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    """
    Retrieves the current authenticated user based on the provided JWT token.

    Args:
        token (str): The JWT token sent by the client.

    Returns:
        dict: A dictionary containing the user's email and ID if the token is valid.

    Raises:
        HTTPException: If the token is invalid or expired, raises a 401 Unauthorized error.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  # Decode the token.
        email = payload.get('sub')
        id = payload.get('id')

        if email is None or id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')
        
        return {'email': email, 'id': id}  # Return user info.

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token expired')  # Token error handling.
