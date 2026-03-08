import asyncio
import time
import re
from googletrans import Translator

INPUT_FILE = "text.txt"      

def split_into_sentences(text: str) -> list[str]:
    """Розбиває текст на речення"""
    pattern = r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s'
    sentences = re.split(pattern, text.strip())
    return [s.strip() for s in sentences if s.strip()]

async def async_detect_and_translate(sentence: str, target_lang: str):
    """Асинхронний детект + переклад одного речення"""
    async with Translator() as translator:
        detect_result = await translator.detect(sentence)
        translated = await translator.translate(sentence, dest=target_lang)
        return {
            'original': sentence,
            'detect_lang': detect_result.lang,
            'confidence': detect_result.confidence,
            'translated': translated.text
        }

async def TransLate(text: str, lang: str) -> str:
    """Синхронна обгортка над асинхронним перекладом"""
    async with Translator() as translator:
        try:
            result = await translator.translate(text, dest=lang)
            return result.text
        except Exception as e:
            return f"Помилка перекладу: {str(e)}"

async def LangDetect(txt: str) -> str:
    """Асинхронна детекція мови"""
    async with Translator() as translator:
        try:
            detection = await translator.detect(txt)
            return f"Мова: {detection.lang}, Впевненість: {detection.confidence:.2f}"
        except Exception as e:
            return f"Помилка визначення мови: {str(e)}"

async def main():
    print("=== Програма перекладу тексту з файлу ===\n")

    #1.Читання файлу
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            full_text = f.read().strip()
        print(f"Ім'я файлу: {INPUT_FILE}")
    except Exception as e:
        print(f"Помилка читання файлу: {e}")
        return

    if not full_text:
        print("Файл порожній")
        return

    #2.Кількість символів і речень
    sentences = split_into_sentences(full_text)
    sentence_count = len(sentences)
    char_count = len(full_text)

    print(f"Кількість символів у тексті: {char_count}")
    print(f"Кількість речень у тексті: {sentence_count}\n")

    # 3.Мова оригінального тексту
    original_lang_info = await LangDetect(full_text[:1500])  
    print("Мова, код та впевненість оригінального тексту:")
    print(original_lang_info)
    print("\nОригінальний текст:")
    print(full_text)
    print("\n" + "="*90 + "\n")

    # 4.Запитуємо код мови перекладу
    user_lang_input = input("На яку мову перекласти текст? (введіть код мови, наприклад: en, uk, fr, de, pl, es тощо): ").strip().lower()
    
    if not user_lang_input:
        print("\nКод мови не введено. Переклад не виконано.")
        return

    target_lang_code = user_lang_input
    print(f"\nПереклад буде виконано на мову: {target_lang_code}\n")

    # Синхронний режим (послідовно)
    print("Виконується синхронний переклад (3.4.1)...")
    start_sync = time.perf_counter()

    sync_translations = []
    for sent in sentences:
        trans = await TransLate(sent, target_lang_code)
        sync_translations.append(trans)

    sync_time = time.perf_counter() - start_sync

    print("Переклад тексту (синхронний режим):")
    print("\n".join(sync_translations))
    print(f"\nЧас визначення мови та перекладу (синхронний режим): {sync_time:.3f} сек\n")

    # Асинхронний режим (паралельно)
    print("Виконується асинхронний переклад (3.4.2)...")
    start_async = time.perf_counter()

    tasks = [async_detect_and_translate(sent, target_lang_code) for sent in sentences]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    async_time = time.perf_counter() - start_async

    print("Переклад тексту (асинхронний режим):")
    for res in results:
        if isinstance(res, Exception):
            print(f"Помилка обробки речення: {res}")
            continue
        print(f"Оригінал: {res['original'][:70]}...")
        print(f"Переклад: {res['translated']}")
        print(f"Детект: {res['detect_lang']} ({res['confidence']:.2f})")
        print("-"*80)

    print(f"\nЧас визначення мови та перекладу (асинхронний режим): {async_time:.3f} сек")

if __name__ == "__main__":
    asyncio.run(main())
