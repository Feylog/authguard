from fastapi import FastAPI
import fastapi
from app.config import Config
from app.database import Base, engine, init_db
from app.routes import auth, protected
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Для боевого окружения укажите конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Сначала регистрируем маршруты, чтобы они не были затенены монтированием
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(protected.router, prefix="/protected", tags=["Protected"])

# Создание таблиц базы данных и добавление синтетических данных
@app.on_event("startup")
def on_startup():
    try:
        Base.metadata.create_all(bind=engine)
        print("Таблицы успешно созданы!")
        init_db()
        print("База данных успешно инициализирована.")
    except Exception as e:
        print(f"Ошибка при инициализации базы данных: {e}")

@app.on_event("startup")
def log_routes():
    print("Список маршрутов:")
    for route in app.router.routes:
        if isinstance(route, fastapi.routing.APIRoute):
            print(f"{route.path} -> {route.name} -> {route.methods}")
        elif isinstance(route, fastapi.routing.Mount):
            print(f"{route.path} -> {route.name} (Static Mount)")
        else:
            print(f"{route.path} -> {route.name} -> (Unknown Route Type)")

# Проверка здоровья приложения
@app.get("/")
def read_root():
    return {"message": "AuthGuard is running!"}

# Монтируем статику после того, как зарегистрированы все другие маршруты
app.mount("/frontend", StaticFiles(directory="frontend", html=True), name="frontend")