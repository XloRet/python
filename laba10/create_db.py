from faker import Faker
from sqlalchemy import create_engine, text
import random
from datetime import datetime, timedelta

fake = Faker('uk_UA')
engine = create_engine("postgresql://user:password@localhost:5432/phone_station")

def create_tables():
    with engine.connect() as conn:
        conn.execute(text("""
            DROP TABLE IF EXISTS calls;
            DROP TABLE IF EXISTS phones;
            DROP TABLE IF EXISTS clients;
            DROP TABLE IF EXISTS tariffs;

            CREATE TABLE clients (
                client_id SERIAL PRIMARY KEY,
                client_type VARCHAR(20) NOT NULL CHECK (client_type IN ('фізична особа', 'відомство')),
                address VARCHAR(200) NOT NULL,
                last_name VARCHAR(80),
                first_name VARCHAR(50),
                middle_name VARCHAR(60)
            );

            CREATE TABLE tariffs (
                tariff_id SERIAL PRIMARY KEY,
                call_type VARCHAR(20) NOT NULL CHECK (call_type IN ('внутрішній', 'міжміський', 'мобільний')),
                price_per_minute NUMERIC(6,2) NOT NULL CHECK (price_per_minute > 0)
            );

            CREATE TABLE phones (
                phone_number VARCHAR(20) PRIMARY KEY,
                client_id INTEGER REFERENCES clients(client_id) ON DELETE CASCADE
            );

            CREATE TABLE calls (
                call_id SERIAL PRIMARY KEY,
                call_date DATE NOT NULL,
                phone_number VARCHAR(20) REFERENCES phones(phone_number) ON DELETE CASCADE,
                minutes INTEGER NOT NULL CHECK (minutes > 0),
                tariff_id INTEGER REFERENCES tariffs(tariff_id)
            );
        """))
        conn.commit()
    print("Таблиці створено успішно.")

def populate_data():
    with engine.connect() as conn:
        # Тарифи
        tariffs = [
            ('внутрішній', 0.50),
            ('міжміський', 2.80),
            ('мобільний', 1.50)
        ]
        for t in tariffs:
            conn.execute(text("INSERT INTO tariffs (call_type, price_per_minute) VALUES (:type, :price)"), 
                        {"type": t[0], "price": t[1]})

        # 5 Клієнтів
        for _ in range(5):
            client_type = 'відомство' if random.random() < 0.3 else 'фізична особа'
            conn.execute(text("""
                INSERT INTO clients (client_type, address, last_name, first_name, middle_name)
                VALUES (:type, :addr, :lname, :fname, :mname)
            """), {
                "type": client_type,
                "addr": fake.address(),
                "lname": fake.last_name(),
                "fname": fake.first_name(),
                "mname": fake.middle_name()
            })

        # 7 Телефонів
        clients = [row[0] for row in conn.execute(text("SELECT client_id FROM clients")).fetchall()]
        for _ in range(7):
            conn.execute(text("""
                INSERT INTO phones (phone_number, client_id)
                VALUES (:phone, :cid)
            """), {
                "phone": fake.numerify(text="0##-###-####"),
                "cid": random.choice(clients)
            })

        # 20 Розмов
        phones = [row[0] for row in conn.execute(text("SELECT phone_number FROM phones")).fetchall()]
        tariffs_ids = [row[0] for row in conn.execute(text("SELECT tariff_id FROM tariffs")).fetchall()]

        start_date = datetime(2026, 4, 1)
        for _ in range(20):
            call_date = start_date + timedelta(days=random.randint(0, 29))
            conn.execute(text("""
                INSERT INTO calls (call_date, phone_number, minutes, tariff_id)
                VALUES (:date, :phone, :min, :tariff)
            """), {
                "date": call_date.date(),
                "phone": random.choice(phones),
                "min": random.randint(1, 45),
                "tariff": random.choice(tariffs_ids)
            })

        conn.commit()
    print("Дані успішно заповнено (5 клієнтів, 7 номерів, 20 розмов).")

if __name__ == "__main__":
    create_tables()
    populate_data()