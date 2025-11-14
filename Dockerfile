# Stage 1: сборка зависимостей
FROM python:3.13-slim AS builder

WORKDIR /app
COPY requirements.txt .
# Устанавливаем в /usr/local (глобально, без --user)
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: финальный образ
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Создаём непривилегированного пользователя
RUN adduser --disabled-password --gecos '' appuser && chown -R appuser /app
USER appuser

# Копируем зависимости из builder-стадии
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Копируем код
COPY . .

# Собираем статику
RUN python manage.py collectstatic --noinput

# Запуск (для dev можно использовать runserver, для prod — gunicorn)
CMD ["gunicorn", "laba2.wsgi:application", "--bind", "0.0.0.0:8000"]