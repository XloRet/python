import googletrans as gt 
from googletrans import Translator

LANGUAGE_ALIASES = {
    'ua': 'uk', 'ukr': 'uk', 'уа': 'uk', 'укр': 'uk',
    'українська': 'uk', 'ukrainian': 'uk',
}

def normalize_lang(lang: str) -> str:
    lang = lang.lower().strip()
    return LANGUAGE_ALIASES.get(lang, lang)

def TransLate(str_text: str, lang: str) -> str:
    if not str_text.strip():
        return "Текст для перекладу порожній"

    try:
        translator = Translator()
        clean_text = str_text.encode('utf-8', errors='ignore').decode('utf-8', errors='replace')
        lang_norm = normalize_lang(lang)
        translated = translator.translate(clean_text, dest=lang_norm)
        return translated.text
    except ValueError as ve:
        if "invalid" in str(ve).lower() or "destination" in str(ve).lower():
            return f"Помилка: мова '{lang}' не розпізнана. Спробуйте 'uk', 'en', 'fr' тощо (пункт 4 — список мов)."
        return f"Помилка перекладу: {str(ve)}"
    except Exception as e:
        err = str(e)
        if "surrogates" in err or "codec can't encode" in err:
            return "Помилка кодування (баг бібліотеки з кирилицею). Спробуйте текст без емодзі/спецсимволів."
        return f"Помилка перекладу: {err}"

def LangDetect(txt: str) -> str:
    if not txt.strip():
        return "Текст порожній"
    try:
        translator = Translator()
        detection = translator.detect(txt)
        return f"Мова: {detection.lang}, Впевненість: {detection.confidence:.2f}"
    except Exception as e:
        return f"Помилка: {str(e)}"

def CodeLang(lang: str) -> str:
    if not lang.strip():
        return "Введіть мову або код"
    try:
        translator = Translator()
        lang_map = translator.LANGUAGES
        lang_norm = normalize_lang(lang)
        if lang_norm in lang_map:
            return lang_map[lang_norm].capitalize()
        for code, name in lang_map.items():
            if name.lower() == lang_norm or name.capitalize() == lang.strip():
                return code
        return f"Мова '{lang}' не знайдена"
    except Exception as e:
        return f"Помилка: {str(e)}"

def show_supported_languages():
    try:
        translator = Translator()
        lang_map = translator.LANGUAGES
        print("\nПідтримувані мови (код → назва):")
        for code in sorted(lang_map):
            print(f"  {code:4} → {lang_map[code].capitalize()}")
        print(f"\nВсього: {len(lang_map)} мов\n")
    except Exception as e:
        print(f"Помилка отримання списку: {str(e)}")

def main():
    print("=== Програма перекладу тексту (googletrans 3.1.0a0) ===")
    print("Команди:")
    print("  1  — переклад тексту")
    print("  2  — визначення мови")
    print("  3  — код ↔ назва мови")
    print("  4  — список мов")
    print("  0  — вихід\n")

    while True:
        choice = input("Виберіть дію (0-4): ").strip()

        if choice == "0":
            print("До побачення!")
            break

        elif choice == "1":
            text = input("Текст для перекладу: ").strip()
            if not text: 
                print("Текст порожній\n"); continue
            lang = input("Мова (en / english / uk / ua): ").strip()
            print(f"Результат: {TransLate(text, lang)}\n")

        elif choice == "2":
            text = input("Текст для аналізу: ").strip()
            if not text: 
                print("Текст порожній\n"); continue
            print(f"Результат: {LangDetect(text)}\n")

        elif choice == "3":
            lang = input("Назва або код мови: ").strip()
            print(f"Результат: {CodeLang(lang)}\n")

        elif choice == "4":
            show_supported_languages()

        else:
            print("Невірний вибір\n")

if __name__ == "__main__":
    main()