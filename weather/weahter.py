#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import os
from datetime import datetime
from dotenv import load_dotenv
import platform

# Завантажуємо змінні з .env файлу (якщо є)
load_dotenv()

# Отримуємо API ключ з змінної середовища
API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")

if not API_KEY:
    print("Помилка: не знайдено змінну OPENWEATHERMAP_API_KEY")
    print("Додайте її в ~/.bashrc або створіть файл .env")
    exit(1)

CITY = input("Введіть назву міста (наприклад: Kyiv, Lviv, London): ").strip()

if not CITY:
    print("Назва міста не може бути порожньою.")
    exit(1)

URL = "https://api.openweathermap.org/data/2.5/weather"
PARAMS = {
    "q": CITY,
    "appid": API_KEY,
    "units": "metric",          # Цельсій, м/с
    "lang": "ua"                # українська мова опису погоди
}

try:
    response = requests.get(URL, params=PARAMS, timeout=10)
    response.raise_for_status()
    data = response.json()
except requests.exceptions.RequestException as e:
    print(f"Помилка підключення до API: {e}")
    exit(1)

if data.get("cod") != 200:
    print(f"Помилка API: {data.get('message', 'Невідома помилка')}")
    exit(1)

temp = data["main"]["temp"]
feels_like = data["main"]["feels_like"]
pressure = data["main"]["pressure"]
humidity = data["main"]["humidity"]
wind_speed = data["wind"]["speed"]
description = data["weather"][0]["description"].capitalize()

sunrise = datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%H:%M")
sunset = datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%H:%M")

request_time = datetime.now().strftime("%Y-%m-%d %H:%M")
timezone = f"UTC{data['timezone']//3600:+d}"

print("\n" + "═" * 60)
print(f"Погода в місті: {data['name']}, {data['sys']['country']}")
print(f"Запит виконано: {request_time}   (часова зона: {timezone})")
print("─" * 60)
print(f"Температура     : {temp} °C")
print(f"Відчувається як : {feels_like} °C")
print(f"Опис            : {description}")
print(f"Вологість       : {humidity} %")
print(f"Тиск            : {pressure} гПа")
print(f"Швидкість вітру : {wind_speed} м/с")
print(f"Схід сонця      : {sunrise}")
print(f"Захід сонця     : {sunset}")
print("═" * 60)




