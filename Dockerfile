# Базовый образ для Python
FROM python:3.10-slim

# Устанавливаем рабочую директорию
WORKDIR /authguard

# Копируем все файлы проекта в контейнер
COPY . /authguard

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Устанавливаем переменную PYTHONPATH
ENV PYTHONPATH=/authguard

# Экспонируем порт
EXPOSE 8000

# Запуск приложения
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]