from urllib.parse import unquote
import pyperclip

print("=== Програма 2: Декодування інтернет-посилань ===\n")

url_encoded = input("Вставте закодоване посилання (з %D0%A8 тощо):\n").strip()

if not url_encoded:
    print("Посилання не введено.")
else:
    # Декодуємо URL
    decoded_url = unquote(url_encoded)

    print("\n" + "─" * 70)
    print("Декодоване посилання:")
    print(decoded_url)
    print("─" * 70)

    # Копіюємо в буфер обміну
    try:
        pyperclip.copy(decoded_url)
        print("✅ Посилання успішно скопійовано в буфер обміну!")
    except Exception as e:
        print(f"Не вдалося скопіювати в буфер: {e}")

print("\nГотово.")