from fastapi import APIRouter, status, HTTPException
from ..models.users_model import UserModel
from datetime import timedelta
from ..schemas.user_schemas import UserRegisterModel, UserLoginModel, Token
from ..utils.utils import db_dependency
from ..utils.user_utils import create_access_token, authenticate_user, hash_password

# Create a router instance for the 'Users' API with the prefix '/api/v1/users'
router = APIRouter(prefix='/api/v1/users', tags=['Users'])

@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserRegisterModel, db: db_dependency):
    """
    Registers a new user by creating a new user record in the database.
    
    - Checks if the user already exists by verifying the email in the database.
    - If the user exists, raises an HTTP 400 error with the message 'User already exists'.
    - If the user does not exist, hashes the provided password and stores the user data in the database.
    - Generates an access token for the newly registered user and returns it in the response.
    
    Args:
        user_data (UserRegisterModel): The data for registering a new user, including email and password.
        db (db_dependency): The database session dependency used to interact with the database.
    
    Returns:
        dict: A dictionary containing the generated access token and the token type ('bearer').
    
    Raises:
        HTTPException: If the user already exists, a 400 error is raised.
    """
    if db.query(UserModel).filter(UserModel.email == user_data.email).first():
        # If a user with the given email already exists, raise a 400 error
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User already exists')

    # Create a new UserModel instance with the provided email and hashed password
    user = UserModel(
        email=user_data.email,
        password_hash=hash_password(user_data.password)
    )
    db.add(user)  # Add the new user to the session
    db.commit()   # Commit the transaction to save the user
    db.refresh(user)  # Refresh the user object to get the generated ID

    # Generate an access token for the new user with an expiration time of 20 minutes
    token = create_access_token(
        user.email,
        user.id,
        timedelta(minutes=20)
    )

    return {'access_token': token, 'token_type': 'bearer'}


@router.post('/login', status_code=status.HTTP_200_OK, response_model=Token)
async def login_user(user_data: UserLoginModel, db: db_dependency):
    """
    Authenticates an existing user and returns an access token.
    
    - Verifies the user's credentials by calling the 'authenticate_user' function.
    - If the credentials are incorrect or the user is not found, raises a 404 HTTP error.
    - If authentication is successful, generates an access token for the user and returns it in the response.
    
    Args:
        user_data (UserLoginModel): The data for logging in, including the email and password.
        db (db_dependency): The database session dependency used to interact with the database.
    
    Returns:
        dict: A dictionary containing the generated access token and the token type ('bearer').
    
    Raises:
        HTTPException: If the user is not found or authentication fails, a 404 error is raised.
    """
    # Authenticate the user by checking the email and password
    user = authenticate_user(user_data.email, user_data.password, db)
    if not user:
        # If authentication fails, raise a 404 error indicating that the user was not found
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

    # Generate an access token for the authenticated user with an expiration time of 20 minutes
    token = create_access_token(
        user.email,
        user.id,
        timedelta(minutes=20)
    )

    return {'access_token': token, 'token_type': 'bearer'}
