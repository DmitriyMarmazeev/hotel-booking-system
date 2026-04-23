#!/bin/sh
echo "Загрузка модели t-tech/T-lite-it-2.1..."
# Ждём пока сервер Ollama начнёт принимать запросы
until /bin/ollama list > /dev/null 2>&1; do
    sleep 2
done
/bin/ollama pull t-tech/T-lite-it-2.1
echo "Модель загружена."
# Бесконечный цикл, чтобы контейнер не завершился (основной процесс serve уже работает)
tail -f /dev/null