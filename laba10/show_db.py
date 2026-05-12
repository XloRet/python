from sqlalchemy import create_engine, text, inspect
from tabulate import tabulate

engine = create_engine("postgresql://user:password@localhost:5432/phone_station")

def show_structure():
    print("\n=== СТРУКТУРА ТАБЛИЦЬ ===")
    inspector = inspect(engine)
    for table_name in inspector.get_table_names():
        print(f"\nТаблиця: {table_name.upper()}")
        for col in inspector.get_columns(table_name):
            print(f"   • {col['name']:20} {col['type']}")

def print_table(table_name, limit=30):
    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT * FROM {table_name} LIMIT {limit}"))
        print(f"\n=== ТАБЛИЦЯ: {table_name.upper()} ===")
        print(tabulate(result.fetchall(), headers=result.keys(), tablefmt="pretty"))

def run_queries():
    with engine.connect() as conn:
        print("\n" + "="*100)
        print("8. ЗАПИТИ ЗА ВАРІАНТОМ")
        print("="*100)

        # 1. Клієнти-фізичні особи
        print("\n1. Клієнти — фізичні особи (відсортовано за прізвищем):")
        q1 = conn.execute(text("""
            SELECT client_id, last_name, first_name, middle_name, address 
            FROM clients 
            WHERE client_type = 'фізична особа'
            ORDER BY last_name;
        """))
        print(tabulate(q1.fetchall(), headers=q1.keys(), tablefmt="pretty"))

        # 2. Кількість клієнтів за типом
        print("\n2. Кількість клієнтів за типом (підсумковий запит):")
        q2 = conn.execute(text("""
            SELECT 
                client_type AS "Тип клієнта",
                COUNT(*) AS "Кількість"
            FROM clients 
            GROUP BY client_type;
        """))
        print(tabulate(q2.fetchall(), headers=q2.keys(), tablefmt="pretty"))

        # 3. Вартість кожної розмови
        print("\n3. Вартість кожної розмови (обчислювальне поле):")
        q3 = conn.execute(text("""
            SELECT 
                c.call_id,
                cl.last_name || ' ' || cl.first_name AS client,
                c.call_date,
                c.minutes,
                t.call_type,
                t.price_per_minute,
                ROUND(c.minutes * t.price_per_minute, 2) AS total_cost
            FROM calls c
            JOIN phones p ON c.phone_number = p.phone_number
            JOIN clients cl ON p.client_id = cl.client_id
            JOIN tariffs t ON c.tariff_id = t.tariff_id
            ORDER BY c.call_date DESC;
        """))
        print(tabulate(q3.fetchall(), headers=q3.keys(), tablefmt="pretty"))

        # 4. Розмови з параметром (мобільний)
        print("\n4. Розмови типу 'мобільний' (запит з параметром):")
        q4 = conn.execute(text("""
            SELECT 
                cl.last_name || ' ' || cl.first_name AS client,
                c.call_date,
                c.minutes,
                t.call_type,
                ROUND(c.minutes * t.price_per_minute, 2) AS cost
            FROM calls c
            JOIN phones p ON c.phone_number = p.phone_number
            JOIN clients cl ON p.client_id = cl.client_id
            JOIN tariffs t ON c.tariff_id = t.tariff_id
            WHERE t.call_type = 'мобільний'
            ORDER BY c.call_date;
        """))
        print(tabulate(q4.fetchall(), headers=q4.keys(), tablefmt="pretty"))

        # 5. Загальна вартість по клієнтах
        print("\n5. Загальна вартість розмов для кожного клієнта (підсумковий):")
        q5 = conn.execute(text("""
            SELECT 
                cl.last_name || ' ' || cl.first_name AS client,
                COUNT(c.call_id) AS calls_count,
                SUM(ROUND(c.minutes * t.price_per_minute, 2)) AS total_cost
            FROM calls c
            JOIN phones p ON c.phone_number = p.phone_number
            JOIN clients cl ON p.client_id = cl.client_id
            JOIN tariffs t ON c.tariff_id = t.tariff_id
            GROUP BY cl.client_id, cl.last_name, cl.first_name
            ORDER BY total_cost DESC;
        """))
        print(tabulate(q5.fetchall(), headers=q5.keys(), tablefmt="pretty"))

        # 6. Перехресний запит (кількість хвилин по типам дзвінків для кожного клієнта)
        print("\n6. Кількість хвилин по типам дзвінків для кожного клієнта (перехресний запит):")
        q6 = conn.execute(text("""
            SELECT 
                cl.last_name || ' ' || cl.first_name AS client,
                SUM(CASE WHEN t.call_type = 'внутрішній' THEN c.minutes ELSE 0 END) AS "Внутрішній",
                SUM(CASE WHEN t.call_type = 'міжміський' THEN c.minutes ELSE 0 END) AS "Міжміський",
                SUM(CASE WHEN t.call_type = 'мобільний' THEN c.minutes ELSE 0 END) AS "Мобільний",
                SUM(c.minutes) AS "Всього хвилин"
            FROM calls c
            JOIN phones p ON c.phone_number = p.phone_number
            JOIN clients cl ON p.client_id = cl.client_id
            JOIN tariffs t ON c.tariff_id = t.tariff_id
            GROUP BY cl.client_id, cl.last_name, cl.first_name
            ORDER BY "Всього хвилин" DESC;
        """))
        print(tabulate(q6.fetchall(), headers=q6.keys(), tablefmt="pretty"))

if __name__ == "__main__":
    show_structure()
    print_table("clients", 10)
    print_table("tariffs")
    print_table("phones")
    print_table("calls", 20)
    run_queries()
    print("\nВсі запити виконані успішно!")