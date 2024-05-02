import logging
from faker import Faker
import psycopg2
from psycopg2 import DatabaseError

fake = Faker()

conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="123456"
)

cur = conn.cursor()

for _ in range(10):
    fullname = fake.name()
    email = fake.email()
    cur.execute("INSERT INTO users (fullname, email) VALUES (%s, %s)", (fullname, email))

for _ in range(20):
    title = fake.sentence(nb_words=3)
    description = fake.text()
    status_id = fake.random_int(min=1, max=3)
    user_id = fake.random_int(min=1, max=10)
    cur.execute("INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)", (title, description, status_id, user_id))

try:
    conn.commit()
except DatabaseError as e:
    logging.error(e)
    conn.rollback()
finally:
    cur.close()
    conn.close()

