import csv
import random
from faker import Faker
from datetime import datetime

# 1. Ініціалізація Faker
fake = Faker(locale='uk_UA')

# 2. Списки по батькові (мінімум 20 записів)
middle_names_male = [
    "Олександрович", "Іванович", "Петрович", "Миколайович", "Васильович", 
    "Григорович", "Дмитрович", "Андрійович", "Сергійович", "Михайлович",
    "Віталійович", "Ігорович", "Юрійович", "Анатолійович", "Євгенович",
    "Степанович", "Володимирович", "Тарасович", "Богданович", "Романович"
]

middle_names_female = [
    "Олександрівна", "Іванівна", "Петрівна", "Миколаївна", "Василівна",
    "Григорівна", "Дмитрівна", "Андріївна", "Сергіївна", "Михайлівна",
    "Віталіївна", "Ігорівна", "Юріївна", "Анатоліївна", "Євгенівна",
    "Степанівна", "Володимирівна", "Тарасівна", "Богданівна", "Романівна"
]

def generate_data(count=500):
    data = []
    # 60% чоловіків (300) та 40% жінок (200)
    male_count = int(count * 0.6)
    female_count = count - male_count
    
    genders = (['Чоловіча'] * male_count) + (['Жіноча'] * female_count)
    random.shuffle(genders)

    for gender in genders:
        if gender == 'Чоловіча':
            first, last = fake.first_name_male(), fake.last_name_male()
            middle = random.choice(middle_names_male)
        else:
            first, last = fake.first_name_female(), fake.last_name_female()
            middle = random.choice(middle_names_female)
            
        # ВСТАНОВЛЕННЯ ДАТИ: від 1946 до 2011 року
        year = random.randint(1946, 2011)
        month = random.randint(1, 12)
        day = random.randint(1, 28) # безпечний вибір для всіх місяців
        birthday = datetime(year, month, day)
        
        data.append([
            last, first, middle, gender, birthday.strftime('%d.%m.%Y'), 
            fake.job(), fake.city(), fake.address().replace('\n', ' '), 
            fake.phone_number(), fake.email()
        ])
    return data

try:
    records = generate_data(500)
    # Зберігаємо з ';' для Excel та правильним кодуванням
    with open('employees.csv', 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f, delimiter=';') 
        writer.writerow([
            "Прізвище", "Ім'я", "По батькові", "Стать", "Дата народження", 
            "Посада", "Місто", "Адреса", "Телефон", "Email"
        ])
        writer.writerows(records)
    print("Файл успішно створено")
except Exception as e:
    print(f"Помилка: {e}")