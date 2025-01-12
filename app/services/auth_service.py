import jwt
from datetime import datetime, timedelta
from app.models.user import User
from app.utils.hashing import Hashing
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate


class AuthService:
    @staticmethod
    def generate_token(user_id, role):
        payload = {
            "user_id": user_id,
            "role": role,
            "exp": datetime.utcnow() + timedelta(hours=1)
        }
        return jwt.encode(payload, "SECRET_KEY", algorithm="HS256")

    @staticmethod
    async def authenticate_user(user_data):
        user = await User.get_by_username(user_data.username)
        if not user or not Hashing.verify(user_data.password, user.password_hash):
            return {"error": "Invalid credentials"}
        token = AuthService.generate_token(user.id, user.role)
        return {"access_token": token, "expires_in": 3600}
    
# Настройка хэширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    SECRET_KEY = "your_secret_key"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60

    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_user(db: Session, user_data: UserCreate):
        user = User(
            username=user_data.username,
            password_hash=AuthService.hash_password(user_data.password)
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def authenticate_user(db: Session, username: str, password: str):
        user = db.query(User).filter(User.username == username).first()
        if user and AuthService.verify_password(password, user.password_hash):
            return user
        return None

    @staticmethod
    def create_access_token(user_id: int):
        payload = {
            "sub": str(user_id),
            "exp": datetime.utcnow() + timedelta(minutes=AuthService.ACCESS_TOKEN_EXPIRE_MINUTES)
        }
        return jwt.encode(payload, AuthService.SECRET_KEY, algorithm=AuthService.ALGORITHM)