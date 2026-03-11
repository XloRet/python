# Використовуємо Python 3.12, як вимагає завдання для сумісності з m2
FROM python:3.12-slim

# Встановлюємо робочу директорію
WORKDIR /app

# Копіюємо всі файли проекту в контейнер
COPY . /app

# Встановлюємо необхідні бібліотеки (САМЕ ЦЬОГО НЕ ВИСТАЧАЛО)
RUN pip install googletrans==3.1.0a0 deep-translator langdetect

# Запускаємо скрипт за замовчуванням
CMD ["python", "gtrans3.py"]docker build -t my-translator .