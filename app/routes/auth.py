from app.schemas.user import UserCreate, TokenResponse
from app.services.auth_service import AuthService
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter()

@router.post("/register", response_model=dict)
def register(user: UserCreate, db: Session = Depends(get_db)):
    from app.models.user import User  # Импорт модели для проверки
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already registered")
    AuthService.create_user(db, user)
    return {"message": "User registered successfully"}

@router.post("/login", response_model=TokenResponse)
def login(user: UserCreate, db: Session = Depends(get_db)):
    authenticated_user = AuthService.authenticate_user(db, user.username, user.password)
    if not authenticated_user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = AuthService.create_access_token(authenticated_user.id)
    return TokenResponse(access_token=token, expires_in=AuthService.ACCESS_TOKEN_EXPIRE_MINUTES * 60)