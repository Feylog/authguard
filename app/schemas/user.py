from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    expires_in: int

class UserLogin(BaseModel):
    username: str
    password: str