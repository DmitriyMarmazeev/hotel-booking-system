# ollama/Dockerfile
FROM ollama/ollama:latest

# Скопируем скрипт для предзагрузки модели
COPY ./load_model.sh /load_model.sh
RUN chmod +x /load_model.sh

# Используем официальный entrypoint, но добавим запуск нашего скрипта в фоне
# Официальный entrypoint запускает сервер Ollama. Мы можем выполнить pull после старта.
ENTRYPOINT ["/bin/sh", "-c"]
CMD ["/bin/ollama serve & sleep 5 && /load_model.sh && wait"]