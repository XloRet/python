import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

try:
    # 1. Зчитування даних (використовуємо той самий розділювач ';')
    df = pd.read_csv('employees.csv', sep=';', encoding='utf-8-sig')
    df['Дата народження'] = pd.to_datetime(df['Дата народження'], dayfirst=True)
    df['Вік'] = df['Дата народження'].apply(lambda x: calculate_age(x.date()))
    print("Ok")

    # Створюємо вікові категорії (згідно з ТЗ)
    bins = [0, 18, 45, 70, 120]
    labels = ['younger_18', '18-45', '45-70', 'older_70']
    df['Категорія'] = pd.cut(df['Вік'], bins=bins, labels=labels, right=False)

    # --- 1. Кількість за статтю ---
    gender_counts = df['Стать'].value_counts()
    print("\nКількість за статтю:")
    print(gender_counts)

    plt.figure(figsize=(8, 6))
    gender_counts.plot(kind='pie', autopct='%1.1f%%', colors=['skyblue', 'pink'], startangle=140)
    plt.title('Розподіл співробітників за статтю')
    plt.ylabel('') # Прибираємо зайвий підпис
    plt.show()

    # --- 2. Кількість за віковими категоріями ---
    age_counts = df['Категорія'].value_counts().sort_index()
    print("\nКількість за віковими категоріями:")
    print(age_counts)

    plt.figure(figsize=(10, 6))
    age_counts.plot(kind='bar', color='lightgreen', edgecolor='black')
    plt.title('Кількість співробітників за віковими категоріями')
    plt.xlabel('Вікова категорія')
    plt.ylabel('Кількість людей')
    plt.xticks(rotation=0)
    plt.show()

    # --- 3. Стать у кожній віковій категорії ---
    gender_age_counts = pd.crosstab(df['Категорія'], df['Стать'])
    print("\nСтать за віковими категоріями:")
    print(gender_age_counts)

    gender_age_counts.plot(kind='bar', figsize=(10, 6), color=['skyblue', 'pink'], edgecolor='black')
    plt.title('Розподіл статі за віковими категоріями')
    plt.xlabel('Вікова категорія')
    plt.ylabel('Кількість людей')
    plt.xticks(rotation=0)
    plt.legend(title='Стать')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

except FileNotFoundError:
    print("Повідомлення про відсутність, або проблеми при відкритті файлу CSV")
except Exception as e:
    print(f"Помилка при аналізі даних: {e}")




    