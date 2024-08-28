import sqlite3
from datetime import datetime


class Pizzas:
    def __init__(self, cursor, connection):
        self.cursor = cursor
        self.connection = connection

    def check_count_pizzas(self, id: int):
        try:
            self.cursor.execute('SELECT count_pizzas FROM list_pizzas WHERE id = ?', (id,))
        except sqlite3.Error as error:
            return [False, error]
        else:
            result = self.cursor.fetchone()
            return [True, str(result[0])]

    def add_count_pizzas(self, add_count: int, id: int):
        count_pizzas = self.check_count_pizzas(id=id)
        if count_pizzas[0] is False:
            return count_pizzas
        try:
            self.cursor.execute('UPDATE list_pizzas SET count_pizzas = ? WHERE id = ?', (int(count_pizzas[1]) +
                                                                                         add_count, id))
            self.connection.commit()
        except sqlite3.Error as error:
            return [False, error]
        else:
            return [True, str(add_count)]

    def remove_count_pizzas(self, remove_count: int, id: int):
        count_pizzas = self.check_count_pizzas(id=id)
        if count_pizzas[0] is False:
            return count_pizzas
        try:
            self.cursor.execute('UPDATE list_pizzas SET count_pizzas = ? WHERE id = ?', (count_pizzas - remove_count, id))
            self.connection.commit()
        except sqlite3.Error as error:
            return [False, error]
        else:
            return [True, str(remove_count)]

    def order_pizza(self, id: int, name: str, phone_number: int, order_date: str):
        count_pizzas = self.check_count_pizzas(id=id)
        if count_pizzas <= 0:
            return [False, "number of pizzas in stock - 0"]
        try:
            self.cursor.execute(
            '''INSERT INTO pizzas (id, name, phone_number, order_date) VALUES (?, ?, ?, ?, ?)''',
            (id, name, phone_number, datetime.now(), 0)
            )
            self.connection.commit()
        except sqlite3.Error as error:
            return [False, error]
        remove_pizzas = self.remove_count_pizzas(remove_count=1, id=id)
        return remove_pizzas[0]

    def complete_order_pizza(self, id: int):
        try:
            self.cursor.execute('UPDATE pizzas SET complete_order = ? WHERE id = ?', (1, id))
            self.connection.commit()
        except sqlite3.Error as error:
            return [False, error]
        else:
            return [True, "complete"]


try:
    sqlite_connection = sqlite3.connect("pizza_python.db")
    cursor = sqlite_connection.cursor()
    pizzas_class = Pizzas(cursor=cursor, connection=sqlite_connection)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pizzas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone_number INTEGER,
        order_date datetime
        complete_order INTEGER);
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS list_pizzas (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        count_pizzas INTEGER);
    """)

    cursor.execute('INSERT OR IGNORE INTO list_pizzas (id, name, count_pizzas) VALUES (0, "Margarita", 0)')
    cursor.execute('INSERT OR IGNORE INTO list_pizzas (id, name, count_pizzas) VALUES (1, "Pepperoni", 0)')
    cursor.execute('INSERT OR IGNORE INTO list_pizzas (id, name, count_pizzas) VALUES (2, "Four cheeses", 0)')

    pizzas_class.check_count_pizzas(id=0)
    cursor.close()

except sqlite3.Error as error:
    print(str(error))
finally:
    if sqlite_connection:
        sqlite_connection.close()
        print("Соединение закрыто")
