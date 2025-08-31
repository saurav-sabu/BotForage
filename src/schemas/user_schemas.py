from pydantic import BaseModel, EmailStr

class UserSignIn(BaseModel):
    email:EmailStr
    password: str

class UserSignUp(BaseModel):
    email:EmailStr
    username:str
    password:str

class UserResponse(BaseModel):
    id:str
    email:EmailStr
    username:str
    is_active:bool

class TokenResponse(BaseModel):
    access_token:str
    token_type:str = "bearer"