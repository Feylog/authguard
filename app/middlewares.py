from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from app.config import Config

# Создаем объект HTTPBearer
security = HTTPBearer()

# Функция проверки токена
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        # Декодирование токена
        token_data = jwt.decode(
            credentials.credentials, 
            Config.SECRET_KEY, 
            algorithms=[Config.ALGORITHM]
        )
        return token_data
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")  # Токен истек
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")  # Неверный токен