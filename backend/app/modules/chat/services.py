import json
import logging
from typing import List, Dict, Any

from langchain_ollama import ChatOllama
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from operator import itemgetter

from app.core.config import settings
from app.core.database import engine  # или используйте строку подключения из settings

logger = logging.getLogger(__name__)

class ChatService:
    def __init__(self):
        # Инициализация LLM (Ollama)
        self.llm = ChatOllama(
            base_url=settings.OLLAMA_BASE_URL,
            model="myhotel-llm:q4_K_M",
            temperature=0.1,   # низкая температура для более детерминированных SQL
        )

        # Подключение к БД через SQLAlchemy engine
        self.db = SQLDatabase(engine)

        # Цепочка для генерации SQL-запроса
        self.generate_query = create_sql_query_chain(self.llm, self.db)

        # Инструмент выполнения SQL
        self.execute_query = QuerySQLDataBaseTool(db=self.db)

        # Цепочка для финального ответа
        answer_prompt = PromptTemplate.from_template("""
Ты — эксперт-консультант по подбору отелей для системы бронирования.
Пользователь спросил: {question}

Для ответа был выполнен SQL запрос: {query}
Результат из базы данных (в формате JSON): {result}

Твоя задача — дать развёрнутый, полезный и дружелюбный ответ на русском языке. 
Выдели наиболее выгодный вариант, опиши удобства номера, цену, город.

**Важно:** В ответе обязательно укажи прямые ссылки на страницы отеля и на страницу бронирования номера в следующем формате:
- Ссылка на отель: `/hotel/<hotel_id>`
- Ссылка на бронирование номера: `/booking/create/<room_id>`

Замени <hotel_id> на реальный UUID отеля из данных, а <room_id> — на UUID комнаты.
Ссылки оформи как обычный текст (не html), например: "Посмотреть отель: /hotel/123e4567-e89b-12d3-a456-426614174000"
Не упоминай технические детали запроса, просто отвечай как консьерж.
""")
        self.rephrase_answer = answer_prompt | self.llm | StrOutputParser()

        # Полная цепочка: вопрос -> генерация SQL -> выполнение -> ответ
        self.chain = (
            RunnablePassthrough.assign(query=self.generate_query)
            .assign(result=itemgetter("query") | self.execute_query)
            | self.rephrase_answer
        )

    async def process_message(self, user_message: str) -> Dict[str, Any]:
        """
        Обрабатывает сообщение пользователя и возвращает ответ ассистента.
        """
        try:
            # Выполняем цепочку (она синхронная, но внутри LangChain может использовать async SQL)
            # Для простоты обернём в асинхронный вызов (можно использовать asyncio.to_thread)
            import asyncio
            response = await asyncio.to_thread(self.chain.invoke, {"question": user_message})

            # Также можно получить последний сгенерированный SQL из контекста (для отладки)
            # В простом варианте мы его не возвращаем, но можно извлечь.
            return {
                "reply": response,
                "sql_query": None  # при желании можно доработать извлечение
            }
        except Exception as e:
            logger.error(f"Ошибка при обработке сообщения: {e}", exc_info=True)
            return {
                "reply": "Извините, произошла ошибка при обработке запроса. Попробуйте позже.",
                "sql_query": None
            }

# Создаём экземпляр сервиса
chat_service = ChatService()