from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
import urllib.parse

from app.core.database import engine
from app.shared.models import Base
from app.modules.auth.models import User
from app.modules.hotels.models import Hotel, RoomType, Room, Pricing
from app.modules.bookings.models import Booking, Payment  # Добавляем новые модели

# Импортируем роутеры
from app.modules.auth.routes import router as auth_router
from app.modules.users.routes import router as users_router
from app.modules.hotels.routes import router as hotels_router
from app.modules.bookings.routes import router as bookings_router  # Новый модуль

# Создаем таблицы
Base.metadata.create_all(bind=engine)

class URLDecodeMiddleware:
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            # Декодируем query parameters
            query_string = scope.get("query_string", b"").decode()
            if query_string:
                decoded_query = urllib.parse.unquote(query_string)
                scope["query_string"] = decoded_query.encode()
        
        await self.app(scope, receive, send)

app = FastAPI(
    title="Hotel Booking System API",
    description="Система управления бронированием номеров в отелях",
    version="1.0.0"
)

app.add_middleware(URLDecodeMiddleware)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(auth_router, prefix="/api/auth", tags=["authentication"])
app.include_router(users_router, prefix="/api/users", tags=["users"])
app.include_router(hotels_router, prefix="/api/hotels", tags=["hotels"])
app.include_router(bookings_router, prefix="/api/bookings", tags=["bookings"])

@app.get("/")
async def root():
    return {"message": "Hotel Booking System API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}