import math

def calculate_areas(a, r):
    """
    Власна функція для обчислення площ.
    Повертає площу квадрата та площу кола, округлені до 2 знаків.
    """
    square_area = a ** 2
    circle_area = math.pi * (r ** 2)
    return round(square_area, 2), round(circle_area, 2)

def get_translation(lang_code):
    """
    Функція для перекладу тексту інтерфейсу.
    Якщо мова не 'uk' або 'en', за замовчуванням повертає українську.
    """
    translations = {
        "uk": {
            "lang_name": "Українська",
            "side": "Сторона квадрата a",
            "radius": "Радіус кола R",
            "sq_area": "Площа квадрата",
            "cir_area": "Площа кола",
            "sq_bigger": "Площа квадрата більше.",
            "cir_bigger": "Площа кола більше.",
            "equal": "Площі рівні."
        },
        "en": {
            "lang_name": "English",
            "side": "Square side a",
            "radius": "Circle radius R",
            "sq_area": "Square area",
            "cir_area": "Circle area",
            "sq_bigger": "The square area is larger.",
            "cir_bigger": "The circle area is larger.",
            "equal": "Areas are equal."
        }
    }
    # Повертає обрану мову або українську за замовчуванням
    return translations.get(lang_code, translations["uk"])

def format_num(num):
    """
    Допоміжна функція для форматування чисел:
    замінює крапку на кому та прибирає .0 у цілих чисел.
    """
    if num == int(num):
        return str(int(num))
    return str(num).replace('.', ',')