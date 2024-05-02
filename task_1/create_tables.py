import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="123456"
)

cur = conn.cursor()

create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        fullname VARCHAR(100),
        email VARCHAR(100) UNIQUE
    )
"""

create_status_table = """
    CREATE TABLE IF NOT EXISTS status (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) UNIQUE
    )
"""

create_tasks_table = """
    CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY,
        title VARCHAR(100),
        description TEXT,
        status_id INTEGER REFERENCES status(id) ON DELETE CASCADE,
        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
    )
"""

cur.execute(create_users_table)
cur.execute(create_status_table)
cur.execute(create_tasks_table)

cur.execute("INSERT INTO status(name) VALUES ('new'), ('in progress'), ('completed')")

conn.commit()

cur.close()
conn.close()