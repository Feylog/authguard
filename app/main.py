from fastapi import FastAPI
import fastapi
from app.config import Config
from app.database import Base, engine, init_db
from app.routes import auth, protected
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Регистрируем маршруты
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(protected.router, prefix="/protected", tags=["Protected"])

# 1. Создаём объект Instrumentator
instrumentator = Instrumentator()

# 2. "Прикрепляем" middleware к приложению (DO NOT do it in startup)
#    Это добавляет middleware метрик (чтобы собирать данные).
instrumentator.instrument(app)

@app.on_event("startup")
async def startup_event():
    """
    Событие при старте приложения.
    """
    try:
        Base.metadata.create_all(bind=engine)
        print("Таблицы успешно созданы!")
        init_db()
        print("База данных успешно инициализирована.")
    except Exception as e:
        print(f"Ошибка при инициализации базы данных: {e}")

    # 3. Только теперь "включаем" эндпоинт /metrics
    #    include_in_schema=True если хотим, чтобы он отображался в /docs
    instrumentator.expose(app, endpoint="/metrics", include_in_schema=True)

    print("Список маршрутов:")
    for route in app.router.routes:
        if isinstance(route, fastapi.routing.APIRoute):
            print(f"{route.path} -> {route.name} -> {route.methods}")
        elif isinstance(route, fastapi.routing.Mount):
            print(f"{route.path} -> {route.name} (Static Mount)")
        else:
            print(f"{route.path} -> {route.name} -> (Unknown Route Type)")

@app.get("/")
def read_root():
    return {"message": "AuthGuard is running!"}

# Подключаем статику
app.mount("/frontend", StaticFiles(directory="frontend", html=True), name="frontend")