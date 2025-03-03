# Використовуємо базовий образ Python
FROM python:3.11

# Встановлюємо робочу директорію для контейнера
WORKDIR /app

# Копіюємо requirements.txt у контейнер
COPY requirements.txt /app/

# Встановлюємо залежності
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо всі файли з локальної папки в контейнер
COPY . /app/

# Запускаємо сервер через uvicorn
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
