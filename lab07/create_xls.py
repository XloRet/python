import pandas as pd
from datetime import date
import os

def calculate_age(born):
    """Рахує кількість повних років на момент поточної дати"""
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def process_to_excel():
    csv_file = 'employees.csv'
    xlsx_file = 'employees.xlsx'

    # 1. Перевірка наявності та відкриття CSV
    try:
        df = pd.read_csv(csv_file, sep=';', encoding='utf-8-sig')
        df['Дата народження'] = pd.to_datetime(df['Дата народження'], dayfirst=True)
    except FileNotFoundError:
        print("Повідомлення про відсутність, або проблеми при відкритті файлу CSV")
        return
    except Exception:
        print("Повідомлення про відсутність, або проблеми при відкритті файлу CSV")
        return

    # 2. Розрахунок віку
    df['Вік'] = df['Дата народження'].apply(lambda x: calculate_age(x.date()))
    
    # Визначаємо колонки для аркушів за категоріями (згідно з картинкою 2)
    cols_to_keep = ["Прізвище", "Ім'я", "По батькові", "Дата народження", "Вік"]

    # 3. Створення XLSX файлу
    try:
        with pd.ExcelWriter(xlsx_file, engine='openpyxl') as writer:
            # Аркуш "all" - всі дані (повна структура з CSV)
            df.to_excel(writer, sheet_name='all', index=False)

            # Функція-помічник для запису категорій з нумерацією №
            def save_category(filter_condition, sheet_name):
                subset = df[filter_condition][cols_to_keep].copy().reset_index(drop=True)
                subset.index += 1  # Нумерація з 1
                subset.to_excel(writer, sheet_name=sheet_name, index_label='№')

            # Аркуш "younger_18"
            save_category(df['Вік'] < 18, 'younger_18')

            # Аркуш "18-45"
            save_category((df['Вік'] >= 18) & (df['Вік'] <= 45), '18-45')

            # Аркуш "45-70"
            save_category((df['Вік'] > 45) & (df['Вік'] <= 70), '45-70')

            # Аркуш "older_70"
            save_category(df['Вік'] > 70, 'older_70')

        print("Ok")

    except Exception:
        print("Повідомлення про неможливість створення XLSX файлу")

if __name__ == "__main__":
    process_to_excel()