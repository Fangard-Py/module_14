import sqlite3


def initiate_db():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    # Создаем таблицу Products, если её еще нет
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Products (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            price INTEGER NOT NULL
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