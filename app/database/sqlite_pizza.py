import aiosqlite
from datetime import datetime
from app.hash import hash_data
from app.debugs.change_logger import logger
from os.path import exists
from secrets import token_hex


class Pizzas_Sqlite:
    def __init__(self, connection):
        self.connection = connection

    async def create_db(self):
        try:
            await self.connection.execute("""
            CREATE TABLE IF NOT EXISTS pizzas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                name TEXT NOT NULL,
                name_pizza TEXT NOT NULL,
                phone_number INTEGER,
                count INTEGER,
                price INTEGER,
                location TEXT NOT NULL,
                order_date datetime,
                complete_order INTEGER);
            """)

            await self.connection.execute("""
            CREATE TABLE IF NOT EXISTS list_pizzas (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                count_pizzas INTEGER,
                price INTEGER,
                description TEXT NOT NULL);
            """)

            await self.connection.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                admin TEXT NOT NULL,
                cookie TEXT NOT NULL);
            """)

            await self.connection.commit()

        except aiosqlite.Error as err:
            logger.error(f"sqlite| Error in create_db: {err}")
            return [False, err]
        logger.debug("sqlite| create_db was successful")
        return [True, "complete"]

    async def create_default(self):
        pizzas_data = [
            (0, "Margarita", 0, 300,
             "Піца “Маргарита” — це класична італійська піца, яка складається з простих, але дуже смачних інгредієнтів. Вона була створена в 1889 році неаполітанським піцайоло Рафаелем Еспозіто на честь королеви Італії Маргарити Савойської"),
            (1, "Pepperoni", 0, 250,
             "Піца “Пепероні” - це класична італійська піца, яка отримала свою назву від основного інгредієнта - ковбаси пепероні. Ця піца відрізняється своїм гострим і пікантним смаком, завдяки якому вона стала популярною у всьому світі."),
            (2, "Four cheese", 0, 300,
             "Чотири сири - різновид піци в італійській кухні, яка укомплектована комбінацією чотирьох видів сиру, зазвичай плавлених разом з томатним соусом.")
        ]

        await self.connection.executemany(
            'INSERT OR IGNORE INTO list_pizzas (id, name, count_pizzas, price, description) VALUES (?, ?, ?, ?, ?)',
            pizzas_data
        )

        test_user_cookie = token_hex(16)

        users_data = [
            (0, "admin", await hash_data(data="admin"), True, 0),
            (1, "sleephat", await hash_data(data="admin"), False, test_user_cookie)
        ]

        await self.connection.executemany('INSERT OR IGNORE INTO users (id, username, password, admin, cookie) VALUES (?, ?, ?, ?, ?)',
                                      users_data
                                          )

        await self.connection.commit()

    async def check_count_pizzas(self, id: int):
        try:
            cursor = await self.connection.execute('SELECT count_pizzas FROM list_pizzas WHERE id = ?', (id,))
            result = await cursor.fetchone()
        except aiosqlite.Error as err:
            logger.error(f"sqlite| Error in check_count_pizzas: {err}")
            return [False, err]
        await cursor.close()
        if result:
            return [True, str(result[0])]
        else:
            return [False, "No pizza found with the given ID"]

    async def delete_by_id_table(self, id: int, table: str):
        try:
            query = f"DELETE FROM {table} WHERE id = ?"
            logger.debug(f"Executing query: {query} with id: {id}")

            await self.connection.execute(query, (id,))
            await self.connection.commit()

        except aiosqlite.Error as err:
            logger.error(f"sqlite| Error in \"delete_id_pizzas\": {err}")
            return [False, err]

        logger.debug(f"sqlite| \"delete_id_pizzas\" completed successfully")
        return [True, "completed"]

    async def change_pizzas(self, id: int, username: str = None, name: str = None, name_pizza: str = None, phone_number: int = None, count: int = None, price: int = None, location: str = None, order_date: datetime = None, complete_order: str = None):
        try:
            if username:
                await self.connection.execute('UPDATE pizzas SET username = ? WHERE id = ?',
                                              (username, id))
            if name:
                await self.connection.execute('UPDATE pizzas SET name = ? WHERE id = ?',
                                              (name, id))
            if name_pizza:
                await self.connection.execute('UPDATE pizzas SET name_pizza = ? WHERE id = ?',
                                              (name_pizza, id))
            if phone_number:
                await self.connection.execute('UPDATE pizzas SET phone_number = ? WHERE id = ?',
                                              (phone_number, id))
            if price:
                await self.connection.execute('UPDATE pizzas SET price = ? WHERE id = ?',
                                              (price, id))
            if count:
                await self.connection.execute('UPDATE pizzas SET count = ? WHERE id = ?',
                                              (count, id))
            if location:
                await self.connection.execute('UPDATE pizzas SET location = ? WHERE id = ?',
                                              (location, id))
            if order_date:
                await self.connection.execute('UPDATE pizzas SET order_date = ? WHERE id = ?',
                                              (order_date, id))
            if complete_order:
                await self.connection.execute('UPDATE pizzas SET complete_order = ? WHERE id = ?',
                                              (order_date, id))
            await self.connection.commit()
        except aiosqlite.Error as err:
            logger.error(f"sqlite| Error in \"change_pizzas\": {err}")
            return [False, err]
        logger.debug(f"sqlite| \"change_pizzas\" completed successfully")
        return [True, "completed"]

    async def change_list_pizzas(self, id: int, name: str = None, price: int = None,
                                 description: str = None):
        try:
            if name:
                await self.connection.execute('UPDATE list_pizzas SET name = ? WHERE id = ?',
                                              (name, id))
            if price:
                await self.connection.execute('UPDATE list_pizzas SET price = ? WHERE id = ?',
                                              (price, id))
            if description:
                await self.connection.execute('UPDATE list_pizzas SET description = ? WHERE id = ?',
                                              (description, id))
            await self.connection.commit()
        except aiosqlite.Error as err:
            logger.error(f"sqlite| Error in \"change_list_pizzas\": {err}")
            return [False, err]
        logger.debug(f"sqlite| \"change_list_pizzas\" completed successfully")
        return [True, "completed"]

    async def add_list_pizzas(self, id: int, name: str = None, count_pizzas: int = None, price: int = None,
                                 description: str = None):
        if id or name or count_pizzas or price or description is None:
            return [False, "not enough information"]
        try:
            await self.connection.execute(
                'INSERT OR IGNORE INTO list_pizzas (id, name, count_pizzas, price, description) VALUES (?, ?, ?, ?, ?)',
                (id, name, count_pizzas, price, description)
            )
            await self.connection.commit()
        except aiosqlite.Error as err:
            logger.error(f"sqlite| Error in \"add_list_pizzas\": {err}")
            return [False, err]
        logger.debug(f"sqlite| \"add_list_pizzas\" completed successfully")
        return [True, "completed"]

    async def check_price_pizzas(self, id: int):
        try:
            cursor = await self.connection.execute('SELECT price FROM list_pizzas WHERE id = ?', (id,))
            result = await cursor.fetchone()
        except aiosqlite.Error as err:
            logger.error(f"sqlite| Error in check_price_pizzas: {err}")
            return [False, err]
        await cursor.close()
        if result:
            return [True, str(result[0])]
        else:
            return [False, "No pizza found with the given ID"]

    async def change_price_pizzas(self, price: int, id: int):
        price_pizza = await self.check_price_pizzas(id=id)
        if not price_pizza[0]:
            logger.error("sqlite| Error in change_price_pizzas: check_price_pizzas failed")
            return price_pizza
        try:
            await self.connection.execute('UPDATE list_pizzas SET price = ? WHERE id = ?', (price, id))
            await self.connection.commit()
        except aiosqlite.Error as err:
            logger.error(f"sqlite| Error in change_price_pizzas: {err}")
            return [False, err]
        logger.debug(f"sqlite| change_price_pizzas completed successfully: {price}")
        return [True, str(price)]

    async def remove_count_pizzas(self, remove_count: int, id: int):
        count_pizzas = await self.check_count_pizzas(id=id)
        if not count_pizzas[0]:
            logger.error("sqlite| Error in remove_count_pizzas: check_count_pizzas failed")
            return count_pizzas
        try:
            change_count_pizzas = int(count_pizzas[1]) - remove_count
            await self.connection.execute('UPDATE list_pizzas SET count_pizzas = ? WHERE id = ?', (change_count_pizzas, id))
            await self.connection.commit()
        except aiosqlite.Error as err:
            logger.error(f"sqlite| Error in remove_count_pizzas: {err}")
            return [False, err]
        logger.debug(f"sqlite| remove_count_pizzas completed successfully: {change_count_pizzas}")
        return [True, str(remove_count)]

    async def order_pizza(self, id: int, name: str, username: str, name_pizza: str, phone_number: int, count: int, price: int, location: str, complete_order: bool = False):
        id_pizza = await self.get_id_pizza(name=name_pizza)
        if id_pizza[0] is False:
            return id_pizza
        logger.debug(f"test/ {id_pizza}")
        count_pizzas = await self.check_count_pizzas(id=id_pizza[1][0])
        if count_pizzas[0] is False:
            logger.error("sqlite| Error in \"order_pizza\": \"check_count_pizzas\" failed")
            return count_pizzas
        elif int(count_pizzas[1]) <= 0:
            err = "Number of pizzas in stock is 0"
            logger.error(f"sqlite| Error in order_pizza: {err}")
            return [False, err]
        try:
            order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if complete_order is False:
                complete_order = 1
            elif complete_order is True:
                complete_order = 2
            await self.connection.execute(
                'INSERT OR IGNORE INTO pizzas (id, name, name_pizza, username, phone_number, count, price, location, order_date, complete_order) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (id, name, name_pizza, username, phone_number, count, price, location, order_date, complete_order)
            )
            await self.connection.commit()
            remove_pizzas = await self.remove_count_pizzas(remove_count=count, id=id_pizza[1][0])
            if remove_pizzas[0] is False:
                logger.error("sqlite| Error in \"order_pizza\": \"remove_count_pizzas\" failed")
                return remove_pizzas
        except aiosqlite.Error as err:
            logger.error(f"sqlite| Error in order_pizza: {err}")
            return [False, err]
        logger.debug(f"sqlite| order_pizza completed successfully: ID {id}, Name {name}, Phone Number {phone_number}")
        return [True, "Order placed"]

    async def complete_order_pizza(self, id: int):
        try:
            await self.connection.execute('UPDATE pizzas SET complete_order = ? WHERE id = ?', ("True", id))
            logger.debug(f"sqlite| execute in function \"complete_order_pizza\"\nid = {id}")
            await self.connection.commit()
            logger.debug("sqlite| commit from function \"complete_order_pizza\"")
        except aiosqlite.Error as err:
            logger.error(f"sqlite| error in function \"complete_order_pizza\"\nerror: {err}")
            return [False, err]
        logger.debug("sqlite| function \"complete_order_pizza\" was complete")
        return [True, "complete"]

    async def check_all_table(self, table: str):
        try:
            cursor = await self.connection.execute(f"SELECT * FROM {table}")
            logger.debug(f"sqlite| execute in function \"check_all_table\"\ntable = {table}")
        except aiosqlite.Error as err:
            logger.error(f"sqlite| error in function \"check_all_table\"\nerror: {err}")
            return [False, err]
        rows = await cursor.fetchall()
        logger.debug("sqlite| function \"check_all_table\" was complete")
        await cursor.close()
        return [True, rows]

    async def check_username(self, username: str):
        try:
            cursor = await self.connection.execute("SELECT * FROM users WHERE username = ?", (username.lower(),))
            logger.debug(f"sqlite| execute in function \"check_all_table\"\nusername = {username.lower()}")
            results = await cursor.fetchone()
        except aiosqlite.Error as err:
            logger.error(f"sqlite| error in function \"check_username\"\nerror: {err}")
            return [False, err]
        logger.debug("sqlite| function \"check_username\" was complete")
        await cursor.close()
        if results:
            return [True, results]
        return [False, "User is not found"]

    async def check_password(self, username: str, password: str):
        exist_username = await self.check_username(username=username)
        if exist_username[0] is False:
            logger.error(f"sqlite| Error in \"check_password\": \"check_username\" failed\nerror: {exist_username[1]}")
            return exist_username
        try:
            cursor = await self.connection.execute("SELECT password FROM users WHERE username = ?", (username,))
        except aiosqlite.Error as err:
            logger.error(f"sqlite| error in function \"check_password\"\nerror: {err}")
            return [False, err]
        result = await cursor.fetchone()
        password_user = result[0]
        hash_password = await hash_data(data=password)
        await cursor.close()
        if password_user == hash_password:
            return [True, hash_password]
        return [False, hash_password]

    async def check_admin(self, username: str):
        exist_username = await self.check_username(username=username)
        if exist_username[0] is False:
            logger.error(f"sqlite| Error in \"check_admin\": \"check_username\" failed\nerror: {exist_username[1]}")
            return exist_username
        try:
            cursor = await self.connection.execute("SELECT admin FROM users WHERE username = ?", (username,))
        except aiosqlite.Error as err:
            logger.error(f"sqlite| error in function \"check_admin\"\nerror: {err}")
            return [False, err]
        result = await cursor.fetchone()
        is_admin = result[0]
        await cursor.close()
        if is_admin == "1":
            return [True, str(is_admin)]
        return [False, str(is_admin)]

    async def create_account(self, username: str, password: str, admin: bool = False):
        username = username.lower()
        password = password.lower()
        exist_username = await self.check_username(username=username)
        if exist_username[0] is True:
            logger.error(f"sqlite| account {username} already created")
            return [False, f"Account {username} already created"]
        try:
            user_cookie = token_hex(16)
            await self.connection.execute(
                'INSERT OR IGNORE INTO users (username, password, admin, cookie) VALUES (?, ?, ?, ?)',
                (username, await hash_data(password), admin, user_cookie)
                )
            await self.connection.commit()
        except aiosqlite.Error as err:
            logger.error(f"sqlite| error in function \"create_account\"\nerror: {err}")
            return [False, "Problem with sqlite\n Please, contact to administrator"]
        return [True, user_cookie]

    async def login_account(self, username: str, password: str):
        exist_username = await self.check_username(username=username)
        if exist_username[0] is False:
            logger.error(f"sqlite| Error in \"check_password\": \"check_username\" failed\nerror: {exist_username[1]}")
            return [False, "Не правильний логін або пароль"]
        try:
            cursor = await self.connection.execute("SELECT password FROM users WHERE username = ?", (username.lower(),))
            cookie_cursor = await self.connection.execute("SELECT cookie FROM users WHERE username = ?", (username.lower(),))
        except aiosqlite.Error as err:
            logger.error(f"sqlite| error in function \"login_account\"\nerror: {err}")
            return [False, err]
        result = await cursor.fetchone()
        password_check = result[0]
        result_cookie = await cookie_cursor.fetchone()
        cookie = result_cookie[0]
        await cursor.close()
        if password_check == await hash_data(password.lower()):
            return [True, cookie]
        return [False, "Не правильний логін або пароль"]

    async def find_username(self, cookie: str):
        try:
            cursor = await self.connection.execute("SELECT username FROM users WHERE cookie = ?", (cookie,))
        except aiosqlite.Error as err:
            logger.error(f"sqlite| error in function \"find_username\"\nerror: {err}")
            return [False, err]
        result = await cursor.fetchone()
        if result is None:
            return [False, "result is none"]
        cookie_check = result[0]
        await cursor.close()
        return [True, cookie_check]

    async def check_user_orders(self, username: str):
        try:
            cursor = await self.connection.execute("SELECT * FROM pizzas WHERE username = ?", (username,))
            result = await cursor.fetchall()
        except aiosqlite.Error as err:
            logger.error(f"sqlite| error in function \"check_user_orders\"\nerror: {err}")
            return [False, err]
        return [True, result]

    async def delete_account(self, cookie: str = None, id: int = None):
        try:
            if cookie:
                await self.connection.execute("DELETE FROM users WHERE cookie = ?", (cookie,))
            elif id:
                await self.connection.execute("DELETE FROM users WHERE id = ?", (id,))
            await self.connection.commit()
        except aiosqlite.Error as err:
            logger.error(f"sqlite| error in function \"delete_account\"\nerror: {err}")
            return [False, err]
        return [True, "deleted"]

    async def get_id_pizza(self, name: str):
        try:
            cursor = await self.connection.execute("SELECT id FROM list_pizzas WHERE name = ?", (name,))
            result = await cursor.fetchone()
        except aiosqlite.Error as err:
            logger.error(f"sqlite| error in function \"get_id_pizza\"\nerror: {err}")
            return [False, err]
        return [True, result]

    async def change_user(self, id: int, username: str, password: str, admin: bool = False):
        try:
            if username:
                await self.connection.execute('UPDATE users SET username = ? WHERE id = ?',
                                              (username, id))
            if password:
                await self.connection.execute('UPDATE users SET password = ? WHERE id = ?',
                                              (await hash_data(password), id))
            await self.connection.execute('UPDATE users SET admin = ? WHERE id = ?',
                                          (admin, id))
            await self.connection.commit()
        except aiosqlite.Error as err:
            logger.error(f"sqlite| Error in \"change_user\": {err}")
            return [False, err]
        logger.debug(f"sqlite| \"change_user\" completed successfully")
        return [True, "completed"]

async def sqlite():
    try:
        sqlite_connection = await aiosqlite.connect(database="app\\database\\pizza_python.db", timeout=30,
                                                    check_same_thread=False)
        logger.debug("sqlite| connected to sqlite database")
        pizzas_class = Pizzas_Sqlite(connection=sqlite_connection)
        if not exists("pizza_python.db"):
            await pizzas_class.create_db()
        await pizzas_class.create_default()
    except aiosqlite.Error as err:
        logger.error(f"sqlite| error in function \"sqlite\"\nerror: {err}")
        return [False, err]
    logger.debug("sqlite| function \"sqlite\" was complete")
    return [True, pizzas_class]

if __name__ == "__main__":
    raise "Please, start main_flask.py"
