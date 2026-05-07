import os

surname = os.getenv('SURNAME')

if surname:
    print(f"Значення змінної SURNAME: {surname}")
else:
    print("Змінна SURNAME не знайдена в системному оточенні.")
