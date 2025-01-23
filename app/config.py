import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY is not set. Add it to your .env file.")
        
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    
    @staticmethod
    def validate_config():
        """
        Проверка обязательных параметров в конфигурации.
        """
        if not Config.SECRET_KEY:
            raise ValueError("SECRET_KEY is missing.")
        if not Config.DATABASE_URL:
            raise ValueError("DATABASE_URL is missing.")