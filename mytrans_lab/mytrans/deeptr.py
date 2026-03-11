# -*- coding: utf-8 -*-
import sys

# Перевірка наявності бібліотек перед запуском
try:
    from deep_translator import GoogleTranslator 
    from langdetect import detect, DetectorFactory, LangDetectException
except ImportError as e:
    print(f"Помилка: Відсутня бібліотека. Встановіть її командою: pip install {e.name}")
    sys.exit()

DetectorFactory.seed = 0  # для відтворюваності

# Отримуємо словник мов: {назва: код}
try:
    LANGUAGES = GoogleTranslator().get_supported_languages(as_dict=True)
except Exception:
    LANGUAGES = {}

def TransLate(text: str, scr: str, dest: str) -> str:
    try:
        # GoogleTranslator очікує назву мови або ISO код. 
        # Якщо scr='auto', він сам визначить мову
        translator = GoogleTranslator(source=scr, target=dest)
        return translator.translate(text)
    except Exception as e:
        return f"Помилка перекладу: {e}"

def LangDetect(text: str, set: str = "all") -> str:
    try:
        lang = detect(text)
        confidence = 1.0  # langdetect не повертає впевненість у методі detect()
        
        if set == "lang":
            return lang
        elif set == "confidence":
            return str(confidence)
        else:
            return f"Lang: {lang}, Confidence: {confidence:.3f}"
    except LangDetectException:
        return "Не вдалося визначити мову"
    except Exception as e:
        return f"Помилка: {e}"

def CodeLang(lang: str) -> str:
    lang = lang.lower()
    # Якщо ввели код (напр. 'uk'), повертаємо назву ('ukrainian')
    for name, code in LANGUAGES.items():
        if code == lang:
            return name.capitalize()
    # Якщо ввели назву (напр. 'ukrainian'), повертаємо код ('uk')
    if lang in LANGUAGES:
        return LANGUAGES[lang]
    
    return "Мова не знайдена"

def LanguageList(out: str = "screen", text: str = None) -> str:
    header = f"{'N':<5} {'Language':<20} {'ISO-639 code':<10}"
    separator = "-" * 40
    rows = [header, separator]
    
    for i, (name, code) in enumerate(LANGUAGES.items(), 1):
        display_name = name.capitalize()
        # Якщо передано текст, перекладаємо назву мови на цільову мову (опціонально)
        if text:
            display_name = TransLate(display_name, 'auto', text)
            
        rows.append(f"{i:<5} {display_name:<20} {code:<10}")
    
    result = "\n".join(rows)
    
    if out == "screen":
        print(result)
        return "Ok"
    return result

# ГОЛОВНИЙ БЛОК ДЛЯ ЗАПУСКУ
if __name__ == "__main__":
    print("--- Програма перекладу активована ---")
    
    test_text = input("Введіть текст для перекладу: ")
    if not test_text:
        test_text = "Привіт, як справи?"

    # 1. Визначення мови
    detected_lang = LangDetect(test_text, "lang")
    print(f"Визначена мова (код): {detected_lang}")

    # 2. Переклад на українську
    # Використовуємо 'auto' або код мови з LangDetect
    res = TransLate(test_text, "auto", "uk")
    print(f"Переклад на українську: {res}")

    # 3. Приклад виводу списку мов (перші 5 для тесту)
    print("\nБажаєте побачити список мов? (так/ні)")
    if input().lower() == "так":
        LanguageList()