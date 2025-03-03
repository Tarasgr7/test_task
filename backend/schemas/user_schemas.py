from pydantic import BaseModel

class UserRegisterModel(BaseModel):
  email:str
  password:str


class UserLoginModel(BaseModel):
  email:str
  password:str

class Token(BaseModel):
    access_token: str
    token_type: str
