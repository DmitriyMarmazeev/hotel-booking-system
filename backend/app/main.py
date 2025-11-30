from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import urllib.parse

from app.core.database import engine
from app.shared.models import Base
from app.modules.auth.models import User
from app.modules.hotels.models import Hotel, RoomType, Room, Pricing
from app.modules.bookings.models import Booking, Payment

# Импортируем роутеры
from app.modules.auth.routes import router as auth_router
from app.modules.users.routes import router as users_router
from app.modules.hotels.routes import router as hotels_router
from app.modules.bookings.routes import router as bookings_router

# Создаем таблицы
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Hotel Booking System API",
    description="Система управления бронированием номеров в отелях",
    version="1.0.0"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Упрощенный middleware для декодирования URL
@app.middleware("http")
async def url_decode_middleware(request: Request, call_next):
    try:
        # Получаем оригинальный query string
        query_string = request.scope.get("query_string", b"").decode('latin-1')
        
        if query_string:
            # Декодируем из URL encoding
            decoded_query = urllib.parse.unquote(query_string, encoding='utf-8')
            # Кодируем обратно в bytes для совместимости
            request.scope["query_string"] = decoded_query.encode('latin-1')
        
        response = await call_next(request)
        return response
        
    except Exception as exc:
        return JSONResponse(
            status_code=500,
            content={"detail": f"Internal server error: {str(exc)}"}
        )

# Глобальный обработчик ошибок
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"}
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