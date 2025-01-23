import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.config import Config

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    SECRET_KEY = Config.SECRET_KEY
    ALGORITHM = Config.ALGORITHM
    ACCESS_TOKEN_EXPIRE_MINUTES = Config.ACCESS_TOKEN_EXPIRE_MINUTES

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Хэширует пароль.
        """
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Проверяет соответствие пароля и хэша.
        """
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_user(db: Session, user_data: UserCreate):
        """
        Создает нового пользователя в базе данных.
        """
        user = User(
            username=user_data.username,
            hashed_password=AuthService.hash_password(user_data.password),
            email=user_data.email,
            role=user_data.role,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def authenticate_user(db: Session, username: str, password: str):
        """
        Аутентифицирует пользователя.
        """
        try:
            user = db.query(User).filter(User.username == username).first()
            if user and AuthService.verify_password(password, user.hashed_password):
                return user
            return None
        except Exception as e:
            raise Exception(f"Ошибка аутентификации: {e}")

    @staticmethod
    def create_access_token(user_id: int):
        """
        Создает JWT токен.
        """
        payload = {
            "sub": str(user_id),
            "exp": datetime.utcnow() + timedelta(minutes=AuthService.ACCESS_TOKEN_EXPIRE_MINUTES),
        }
        return jwt.encode(payload, AuthService.SECRET_KEY, algorithm=AuthService.ALGORITHM)
    @staticmethod
    def verify_user_password_in_db(db: Session, username: str,  plain_password: str):
        """
        Временная функция для проверки, соответствует ли пароль из базы данных введенному.
        """
        user = db.query(User).filter(User.username == username).first()
        if not user:
            return "User not found in database"
        
        if AuthService.verify_password(plain_password, user.hashed_password):
            return "Password is correct"
        else:
            return "Password is incorrect"