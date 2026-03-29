import re

def custom_sort_key(word):
    # Створюємо рядок для правильного порядку українських літер
    ukr_alphabet = "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя"
    
    word_low = word.lower()
    is_ukrainian = bool(re.match(r'[а-щьюяіїєґ]', word_low))
    
    if is_ukrainian:
        # Перетворюємо кожну літеру слова на її індекс в алфавіті
        # Це змусить "є" стояти після "д", а не в кінці
        return (0, [ukr_alphabet.find(c) if c in ukr_alphabet else ord(c) for c in word_low])
    else:
        return (1, word_low)

def main():
    try:
        with open("input.txt", "r", encoding="utf-8") as f:
            text = f.read()
            print("--- Вхідний текст ---")
            print(text)

        # Витягуємо слова, ігноруючи розділові знаки
        words = re.findall(r'\b\w+\b', text)
        
        # Сортування за вашим правилом
        sorted_words = sorted(words, key=custom_sort_key)

        print("\n--- Відсортований список слів ---")
        print(sorted_words)
    except FileNotFoundError:
        print("Помилка: Файл input.txt не знайдено.")

if __name__ == "__main__":
    main()