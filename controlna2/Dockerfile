# Dockerfile для ternovyi
FROM python:3.11-slim

# Встановлюємо потрібні пакети
RUN apt-get update && apt-get install -y \
    nano \
    && rm -rf /var/lib/apt/lists/*

# Створюємо папку з вашим прізвищем
WORKDIR /ternovyi

# Копіюємо всі ваші програми в контейнер
COPY *.py /ternovyi/


RUN chmod +x /ternovyi/*.py

CMD ["/bin/bash"]