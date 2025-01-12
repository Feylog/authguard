from fastapi import FastAPI
from app.config import Config
from app.database import Base, engine
from app.routes import auth, protected

# Создание объекта приложения FastAPI
app = FastAPI(
    title="AuthGuard",
    description="Микросервис для аутентификации и авторизации",
    version="1.0.0"
)

# Подключение маршрутов
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(protected.router, prefix="/protected", tags=["Protected"])

# Инициализация базы данных (создание таблиц, если их нет)
Base.metadata.create_all(bind=engine)

# Здоровье приложения (health-check)
@app.get("/")
def read_root():
    return {"message": "AuthGuard is running!"}