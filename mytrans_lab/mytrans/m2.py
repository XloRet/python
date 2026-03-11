# -*- coding: utf-8 -*-
import sys
from googletrans import Translator, LANGUAGES

# Перевірка версії Python (Пункт 5 завдання)
if sys.version_info >= (3, 13):
    print("googletrans 3.1.0a0 не підтримується в Python 3.13+")
    sys.exit(1)

def TransLate(text: str, scr: str, dest: str) -> str:
    try:
        translator = Translator()
        res = translator.translate(text, src=scr, dest=dest)
        return res.text
    except Exception as e:
        return f"Помилка перекладу (m2): {e}"

def LangDetect(text: str, set: str = "all") -> str:
    try:
        translator = Translator()
        det = translator.detect(text)
        if set == "lang": return det.lang
        if set == "confidence": return str(det.confidence)
        return f"Lang: {det.lang}, Confidence: {det.confidence}"
    except Exception as e:
        return f"Помилка визначення мови (m2): {e}"

def CodeLang(lang: str) -> str:
    lang = lang.lower()
    if lang in LANGUAGES:
        return LANGUAGES[lang]
    for code, name in LANGUAGES.items():
        if name.lower() == lang:
            return code
    return "Помилка: мову не знайдено"

def LanguageList(out: str = "screen", text: str = None) -> str:
    header = f"{'N':<5} {'Language':<20} {'ISO-639':<10} {'Text' if text else ''}"
    rows = [header, "-" * 60]
    
    # Виведемо перші 10 мов для демонстрації
    items = list(LANGUAGES.items())[:10]
    for i, (code, name) in enumerate(items, 1):
        row = f"{i:<5} {name:<20} {code:<10}"
        if text:
            row += f" {TransLate(text, 'auto', code)}"
        rows.append(row)
    
    result = "\n".join(rows)
    if out == "screen":
        print(result)
        return "Ok"
    else:
        with open("lang_list_m2.txt", "w", encoding="utf-8") as f:
            f.write(result)
        return "Ok"