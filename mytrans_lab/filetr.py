import os
import configparser
import importlib

# 1. Читання конфігурації
config = configparser.ConfigParser()
config.read("config.ini", encoding="utf-8")

c = config["DEFAULT"]
input_f = c["input_file"]
lang_to = c["dest_lang"]
mod_name = c["module"]  # m1, m2 або m3
out_mode = c["output"]
max_s = int(c["sentences"])

# 2. Динамічний імпорт модуля
try:
    lib = importlib.import_module(f"mytrans.{mod_name}")
except ImportError:
    print(f"Помилка: Модуль mytrans.{mod_name} не знайдено.")
    exit()

# 3. Перевірка та читання файлу
if not os.path.exists(input_f):
    print(f"Помилка: Файл {input_f} не знайдено.")
    exit()

with open(input_f, "r", encoding="utf-8") as f:
    text = f.read()

# 4. Вивід статистики (Пункт 11.I)
print(f"Файл: {input_f}")
print(f"Розмір файлу: {os.path.getsize(input_f)} байт")
print(f"Кількість символів: {len(text)}")
sentences = [s.strip() for s in text.split(".") if s.strip()]
print(f"Кількість речень: {len(sentences)}")
print("-" * 30)

# 5. Визначення мови та переклад (Пункт 11.II)
# Беремо вказану кількість речень
text_to_translate = ". ".join(sentences[:max_s]) + "."

# Викликаємо функції з підключеного модуля 'lib'
detected_lang = lib.LangDetect(text_to_translate, "lang")
translated_text = lib.TransLate(text_to_translate, "auto", lang_to)

# 6. Вивід результату (Пункт 11.IV-V)
if out_mode == "screen":
    print(f"Модуль: {mod_name}")
    print(f"Вихідна мова (визначено): {detected_lang}")
    print(f"Мова перекладу: {lang_to}")
    print(f"Результат:\n{translated_text}")
else:
    # Формуємо ім'я файлу: input_en.txt
    file_name = os.path.splitext(input_f)[0]
    out_f = f"{file_name}_{lang_to}.txt"
    with open(out_f, "w", encoding="utf-8") as f:
        f.write(translated_text)
    print(f"Результат збережено у файл: {out_f}")