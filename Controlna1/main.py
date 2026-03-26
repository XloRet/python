import json
import os
from utils import calculate_areas, get_translation, format_num

# Назва файлу для збереження даних
FILENAME = "MyData.json"


def main():
    # 1. Перевірка наявності файлу MyData
    if not os.path.exists(FILENAME):
        # Приклад 1: Файлу немає або дані некоректні
        try:
            a_input = float(input("Введіть сторону квадрата a: "))
            r_input = float(input("Введіть радіус кола R: "))
            lang_input = input("Введіть мову інтерфейсу: ").strip().lower()

            # Зберігаємо дані у словник
            data_to_save = {
                "a": a_input,
                "r": r_input,
                "lang": lang_input
            }

            # Записуємо у файл JSON
            with open(FILENAME, 'w', encoding='utf-8') as f:
                json.dump(data_to_save, f, ensure_ascii=False, indent=4)

            print(f"Дані збережено в файл {FILENAME}")
        except ValueError:
            print("Помилка: введіть коректні чисельні значення.")

        # Після збереження програма припиняє роботу за ТЗ
        return

    # 2. При успішному зчитуванні даних з файлу (Приклад 2)
    try:
        with open(FILENAME, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Отримуємо дані з файлу
        a = data.get("a")
        r = data.get("r")
        lang_code = data.get("lang", "uk")

        # Отримуємо переклад та результати обчислень
        t = get_translation(lang_code)
        square_s, circle_s = calculate_areas(a, r)

        # Вивід результатів точно за прикладом у ТЗ
        print(f"Мова: {t['lang_name']}")
        print(f"{t['side']}: {format_num(a)}")
        print(f"{t['radius']}: {format_num(r)}")
        print(f"{t['sq_area']}: {format_num(square_s)}")
        print(f"{t['cir_area']}: {format_num(circle_s)}")

        # Визначення, яка площа більша
        if square_s > circle_s:
            print(t['sq_bigger'])
        elif circle_s > square_s:
            print(t['cir_bigger'])
        else:
            print(t['equal'])

    except (json.JSONDecodeError, KeyError, ValueError):
        # Якщо дані в файлі некоректні, просимо ввести наново
        print("Виявлено некоректні дані у файлі. Спробуйте ввести їх ще раз.")
        if os.path.exists(FILENAME):
            os.remove(FILENAME)
        main()


if __name__ == "__main__":
    main()