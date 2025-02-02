import sqlite3


def initiate_db():
    with sqlite3.connect('products.db') as conn:
        cursor = conn.cursor()

        # Создаем таблицу Products, если её еще нет
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Products (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT,
                price REAL NOT NULL
            )
        ''')

        # Создаем таблицу Users, если её еще нет
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                email TEXT NOT NULL,
                age INTEGER NOT NULL,
                balance INTEGER NOT NULL DEFAULT 1000
            )
        ''')

        conn.commit()
        conn.close()


def get_all_products():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    # Получаем все продукты из базы данных
    cursor.execute("SELECT * FROM Products")
    products = cursor.fetchall()

    conn.close()
    return products


def add_user(username, email, age):
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO Users (username, email, age) VALUES (?, ?, ?)",
            (username, email, age)
        )
        conn.commit()
    except sqlite3.IntegrityError as e:
        print(f"Пользователь с таким именем или почтой уже существует: {e}")
    finally:
        conn.close()


def is_included(username):
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM Users WHERE username = ?", (username,))
    count = cursor.fetchone()[0]

    conn.close()
    return bool(count)

# # Инициализируем базу данных
# initiate_db()
#
# conn = sqlite3.connect('products.db')
# cursor = conn.cursor()
#
# # Добавляем несколько продуктов
# cursor.execute("INSERT INTO Products (title, description, price) VALUES ('Продукт 1', 'Описание продукта 1', 100)")
# cursor.execute("INSERT INTO Products (title, description, price) VALUES ('Продукт 2', 'Описание продукта 2', 200)")
# cursor.execute("INSERT INTO Products (title, description, price) VALUES ('Продукт 3', 'Описание продукта 3', 300)")
# cursor.execute("INSERT INTO Products (title, description, price) VALUES ('Продукт 4', 'Описание продукта 4', 400)")
#
# conn.commit()
# conn.close()
