from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import Config
import bcrypt
import logging

# URL базы данных
SQLALCHEMY_DATABASE_URL = Config.DATABASE_URL

# Настройка SQLAlchemy
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()

# Логгирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация базы данных (синтетические данные)
def init_db():
    try:
        from app.models.user import User  # Импорт внутри функции для избежания циклических зависимостей
        db = SessionLocal()

        # Создание таблиц
        Base.metadata.create_all(bind=engine)

        # Синтетические данные
        users = [
            {"username": "testuser1", "password": "password", "email": "test1@example.com", "role": "user"},
            {"username": "testuser2", "password": "password", "email": "test2@example.com", "role": "admin"},
        ]

        for user_data in users:
            # Проверка, существует ли пользователь
            existing_user = db.query(User).filter(User.username == user_data["username"]).first()
            if not existing_user:
                # Хеширование пароля
                hashed_password = bcrypt.hashpw(user_data["password"].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                # Создание пользователя
                user = User(
                    username=user_data["username"],
                    hashed_password=hashed_password,
                    email=user_data["email"],
                    role=user_data["role"],
                )
                db.add(user)
        db.commit()
        logger.info("Синтетические данные успешно добавлены!")
    except Exception as e:
        logger.error(f"Ошибка при добавлении данных: {e}")
    finally:
        db.close()

# Dependency для получения сессии
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()