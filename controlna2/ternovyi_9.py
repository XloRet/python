
def main():
    print("=== Обчислення значення полінома (Варіант 9) ===\n")
    
    coeffs = [-2.0, 2.0, 0.0, -15.0, 1.0, 2.0, 7.0]
    
    # Виведення масиву в один рядок з кольором
    print("Масив коефіцієнтів: ", end="")
    for coef in coeffs:
        print(f"\033[34m{coef}\033[0m", end=" ")  # Синій колір для чисел
    print()  # новий рядок
    
    # Виведення кількості елементів з кольором
    print(f"Кількість елементів: \033[32m{len(coeffs)}\033[0m\n")  # Зелений колір
    
    print("Введіть дійсне число x:")
    try:
        x_str = input().strip()
        x = float(x_str.replace(',', '.'))
    except ValueError:
        print("Помилка: введіть коректне дійсне число!")
        return
    
    # Обчислення полінома за схемою Горнера
    result = 0.0
    for a in reversed(coeffs):
        result = result * x + a
    
    # Виведення результату
    print(f"\nP({x}) = {result}")
    
    if abs(result) > 2_000_000_000:
        print("\033[31mУВАГА: Переповнення! Значення більше 2 000 000 000.\033[0m")
    else:
        print(f"P({x}) = \033[33m{result:.2f}\033[0m")  # Жовтий для результату


if __name__ == "__main__":
    main()