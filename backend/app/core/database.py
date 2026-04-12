from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)

# Retry логика для подключения к БД
def create_engine_with_retry(database_url, max_retries=5, delay=5):
    for attempt in range(max_retries):
        try:
            engine = create_engine(
                database_url,
                pool_pre_ping=True,  # Проверяет соединение перед использованием
                pool_recycle=300,    # Переподключается каждые 5 минут
            )
            # Тестируем соединение
            with engine.connect() as conn:
                pass
            logger.info("✅ Database connection successful")
            return engine
        except Exception as e:
            logger.warning(f"❌ Database connection attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                logger.info(f"🔄 Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                logger.error("💥 All database connection attempts failed")
                raise

# Создаем engine с retry логикой
engine = create_engine_with_retry(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency для получения сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()