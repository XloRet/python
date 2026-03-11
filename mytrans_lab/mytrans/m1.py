# -*- coding: utf-8 -*-
from deep_translator import GoogleTranslator
from langdetect import detect, detect_langs

# Словник мов для сумісності з googletrans (додайте більше за потреби)
LANGUAGES = {'uk': 'ukrainian', 'en': 'english', 'fr': 'french', 'de': 'german'}

def TransLate(text: str, scr: str, dest: str) -> str:
    try:
        # deep-translator працює стабільно і синхронно
        translated = GoogleTranslator(source=scr, target=dest).translate(text)
        return translated
    except Exception as e:
        return f"Помилка: {e}"

def LangDetect(text: str, set: str = "all") -> str:
    try:
        lang = detect(text)
        if set == "lang": return lang
        
        # Для коефіцієнта довіри
        probs = detect_langs(text)
        conf = probs[0].prob if probs else 0
        
        if set == "confidence": return str(conf)
        return f"Lang: {lang}, Confidence: {conf}"
    except Exception as e:
        return f"Помилка: {e}"

def CodeLang(lang: str) -> str:
    lang = lang.lower()
    # Пошук за кодом
    if lang in LANGUAGES: return LANGUAGES[lang]
    # Пошук за назвою
    for code, name in LANGUAGES.items():
        if name == lang: return code
    return "Мова не знайдена"

def LanguageList(out: str = "screen", text: str = None) -> str:
    header = f"{'N':<5} {'Language':<15} {'ISO-639':<10}"
    if text: header += f" {'Translated Text':<20}"
    rows = [header, "-" * 50]
    
    test_langs = list(LANGUAGES.items())[:10]
    for i, (code, name) in enumerate(test_langs, 1):
        row = f"{i:<5} {name:<15} {code:<10}"
        if text:
            row += f" {TransLate(text, 'auto', code)}"
        rows.append(row)
    
    res = "\n".join(rows)
    if out == "screen":
        print(res)
    else:
        with open("lang_list.txt", "w", encoding="utf-8") as f:
            f.write(res)
    return "Ok"