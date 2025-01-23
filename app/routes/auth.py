from app.schemas.user import UserCreate, TokenResponse, UserLogin
from app.services.auth_service import AuthService
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
import logging

router = APIRouter()

# Логгирование
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@router.post("/register", response_model=dict, status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    Регистрация нового пользователя.
    """
    try:
        from app.models.user import User  # Импорт модели для проверки
        existing_user = db.query(User).filter(User.username == user.username).first()
        if existing_user:
            logger.warning(f"Попытка повторной регистрации для пользователя: {user.username}")
            raise HTTPException(status_code=400, detail="Username already registered")
        AuthService.create_user(db, user)
        logger.info(f"Пользователь {user.username} успешно зарегистрирован.")
        return {"message": "User registered successfully"}
    except HTTPException as http_exc:
        logger.error(f"Ошибка регистрации: {http_exc.detail}")
        raise
    except Exception as e:
        logger.error(f"Непредвиденная ошибка при регистрации пользователя {user.username}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/login", response_model=TokenResponse, status_code=200)
def login(user: UserLogin, db: Session = Depends(get_db)):
    """
    Авторизация пользователя.
    """
    try:
        logger.info(f"Запрос авторизации для пользователя: {user.username}")
        authenticated_user = AuthService.authenticate_user(db, user.username, user.password)
        if not authenticated_user:
            logger.warning(f"Неверные учетные данные для пользователя: {user.username}")
            raise HTTPException(status_code=401, detail="Invalid username or password")
        token = AuthService.create_access_token(authenticated_user.id)
        logger.info(f"Токен успешно создан для пользователя: {user.username}")
        return TokenResponse(access_token=token, expires_in=AuthService.ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    except HTTPException as http_exc:
        logger.error(f"Ошибка авторизации: {http_exc.detail}")
        raise
    except Exception as e:
        logger.error(f"Непредвиденная ошибка при авторизации пользователя {user.username}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")