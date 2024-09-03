import aiosqlite
from datetime import datetime
from app.hash import hash_data
from app.debugs.change_logger import logger


class Pizzas_Sqlite:
    def __init__(self, connection):
        self.connection = connection

    async def create_db(self):
        try:
            await self.connection.execute("""
            CREATE TABLE IF NOT EXISTS pizzas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone_number INTEGER,
                location TEXT NOT NULL,
                order_date datetime,
                complete_order TEXT NOT NULL);
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
                password TEXT NOT NULL);
            """)

            await self.connection.commit()

        except aiosqlite.Error as error:
            logger.error(f"sqlite| Error in create_db: {error}")
            return [False, error]
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

        hashed_password = await hash_data("admin")

        await self.connection.execute('INSERT OR IGNORE INTO users (id, username, password) VALUES (?, ?, ?)',
                                      (0, "admin", hashed_password))

        await self.connection.commit()

    async def check_count_pizzas(self, id: int):
        try:
            cursor = await self.connection.execute('SELECT count_pizzas FROM list_pizzas WHERE id = ?', (id,))
            result = await cursor.fetchone()
        except aiosqlite.Error as error:
            logger.error(f"sqlite| Error in check_count_pizzas: {error}")
            return [False, error]
        await cursor.close()
        if result:
            return [True, str(result[0])]
        else:
            return [False, "No pizza found with the given ID"]

    async def delete_id_pizzas(self, id: int, table: str):
        try:
            query = f"DELETE FROM {table} WHERE id = ?"
            logger.debug(f"Executing query: {query} with id: {id}")

            await self.connection.execute(query, (id,))
            await self.connection.commit()

        except aiosqlite.Error as error:
            logger.error(f"sqlite| Error in \"delete_id_pizzas\": {error}")
            return [False, error]

        logger.debug(f"sqlite| \"delete_id_pizzas\" completed successfully")
        return [True, "completed"]

    async def change_pizzas(self, id: int, name: str = None, phone_number: int = None, location: str = None, order_date: datetime = None, complete_order: str = None):
        try:
            if name:
                await self.connection.execute('UPDATE pizzas SET name = ? WHERE id = ?',
                                              (name, id))
            if phone_number:
                await self.connection.execute('UPDATE pizzas SET phone_number = ? WHERE id = ?',
                                              (phone_number, id))
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
        except aiosqlite.Error as error:
            logger.error(f"sqlite| Error in \"change_pizzas\": {error}")
            return [False, error]
        logger.debug(f"sqlite| \"change_pizzas\" completed successfully")
        return [True, "completed"]

    async def change_list_pizzas(self, id: int, name: str = None, count_pizzas: int = None, price: int = None,
                                 description: str = None):
        try:
            if name:
                await self.connection.execute('UPDATE list_pizzas SET name = ? WHERE id = ?',
                                              (name, id))
            if count_pizzas:
                await self.connection.execute('UPDATE list_pizzas SET count_pizzas = ? WHERE id = ?',
                                              (count_pizzas, id))
            if price:
                await self.connection.execute('UPDATE list_pizzas SET price = ? WHERE id = ?',
                                              (price, id))
            if description:
                await self.connection.execute('UPDATE list_pizzas SET description = ? WHERE id = ?',
                                              (description, id))
            await self.connection.commit()
        except aiosqlite.Error as error:
            logger.error(f"sqlite| Error in \"change_list_pizzas\": {error}")
            return [False, error]
        logger.debug(f"sqlite| \"change_list_pizzas\" completed successfully")
        return [True, "completed"]

    async def add_pizzas(self, id: int, name: str, phone_number: int, location: str, complete_order: str):
        try:
            await self.connection.execute(
                'INSERT OR IGNORE INTO pizzas (id, name, phone_number, location, order_date, complete_order) VALUES (?, ?, ?, ?, ?, ?)',
                (id, name, phone_number, location, datetime.now(), complete_order)
            )
            await self.connection.commit()
        except aiosqlite.Error as error:
            logger.error(f"sqlite| Error in \"add_pizzas\": {error}")
            return [False, error]
        logger.debug(f"sqlite| \"add_pizzas\" completed successfully")
        return [True, "completed"]

    async def add_list_pizzas(self, id: int, name: str = None, count_pizzas: int = None, price: int = None,
                                 description: str = None):
        try:
            await self.connection.execute(
                'INSERT OR IGNORE INTO list_pizzas (id, name, count_pizzas, price, description) VALUES (?, ?, ?, ?, ?)',
                (id, name, count_pizzas, price, description)
            )
            await self.connection.commit()
        except aiosqlite.Error as error:
            logger.error(f"sqlite| Error in \"add_list_pizzas\": {error}")
            return [False, error]
        logger.debug(f"sqlite| \"add_list_pizzas\" completed successfully")
        return [True, "completed"]

    async def check_price_pizzas(self, id: int):
        try:
            cursor = await self.connection.execute('SELECT price FROM list_pizzas WHERE id = ?', (id,))
            result = await cursor.fetchone()
        except aiosqlite.Error as error:
            logger.error(f"sqlite| Error in check_price_pizzas: {error}")
            return [False, error]
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
        except aiosqlite.Error as error:
            logger.error(f"sqlite| Error in change_price_pizzas: {error}")
            return [False, error]
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
        except aiosqlite.Error as error:
            logger.error(f"sqlite| Error in remove_count_pizzas: {error}")
            return [False, error]
        logger.debug(f"sqlite| remove_count_pizzas completed successfully: {change_count_pizzas}")
        return [True, str(remove_count)]

    async def order_pizza(self, id: int, name: str, phone_number: int):
        count_pizzas = await self.check_count_pizzas(id=id)
        if not count_pizzas[0]:
            logger.error("sqlite| Error in order_pizza: check_count_pizzas failed")
            return count_pizzas
        elif int(count_pizzas[1]) <= 0:
            error = "Number of pizzas in stock is 0"
            logger.error(f"sqlite| Error in order_pizza: {error}")
            return [False, error]
        try:
            order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            await self.connection.execute(
                '''INSERT INTO pizzas (id, name, phone_number, order_date, complete_order) VALUES (?, ?, ?, ?, ?)''',
                (id, name, phone_number, order_date, "False")
            )
            await self.connection.commit()
            remove_pizzas = await self.remove_count_pizzas(remove_count=1, id=id)
            if not remove_pizzas[0]:
                logger.error("sqlite| Error in order_pizza: remove_count_pizzas failed")
                return remove_pizzas
        except aiosqlite.Error as error:
            logger.error(f"sqlite| Error in order_pizza: {error}")
            return [False, error]
        logger.debug(f"sqlite| order_pizza completed successfully: ID {id}, Name {name}, Phone Number {phone_number}")
        return [True, "Order placed"]

    async def complete_order_pizza(self, id: int):
        try:
            await self.connection.execute('UPDATE pizzas SET complete_order = ? WHERE id = ?', ("True", id))
            logger.debug(f"sqlite| execute in function \"complete_order_pizza\"\nid = {id}")
            await self.connection.commit()
            logger.debug("sqlite| commit from function \"complete_order_pizza\"")
        except aiosqlite.Error as error:
            logger.error(f"sqlite| error in function \"complete_order_pizza\"\n error: {error}")
            return [False, error]
        logger.debug("sqlite| function \"complete_order_pizza\" was complete")
        return [True, "complete"]

    async def check_all_table(self, table: str):
        try:
            cursor = await self.connection.execute(f"SELECT * FROM {table}")
            logger.debug(f"sqlite| execute in function \"check_all_table\"\ntable = {table}")
        except aiosqlite.Error as error:
            logger.error(f"sqlite| error in function \"check_all_table\"\n error: {error}")
            return [False, error]
        rows = await cursor.fetchall()
        logger.debug("sqlite| function \"check_all_table\" was complete")
        await cursor.close()
        return [True, rows]

    async def check_username(self, username: str):
        try:
            cursor = await self.connection.execute("SELECT * FROM users WHERE username = ?", (username,))
            logger.debug(f"sqlite| execute in function \"check_all_table\"\nusername = {username}")
            results = await cursor.fetchone()
        except aiosqlite.Error as error:
            logger.error(f"sqlite| error in function \"check_username\"\n error: {error}")
            return [False, error]
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
        except aiosqlite.Error as error:
            logger.error(f"sqlite| error in function \"check_password\"\n error: {error}")
            return [False, error]
        result = await cursor.fetchone()
        password_user = result[0]
        hash_password = await hash_data(password)
        await cursor.close()
        if password_user == hash_password:
            return [True, hash_password]
        return [False, hash_password]


async def sqlite():
    try:
        sqlite_connection = await aiosqlite.connect(database="app\\database\\pizza_python.db", timeout=30,
                                                    check_same_thread=False)
        logger.debug("sqlite| connected to sqlite database")
        pizzas_class = Pizzas_Sqlite(connection=sqlite_connection)
    except aiosqlite.Error as error:
        logger.error(f"sqlite| error in function \"sqlite\"\n error: {error}")
        return [False, error]
    logger.debug("sqlite| function \"sqlite\" was complete")
    return [True, pizzas_class]

if __name__ == "__main__":
    raise "Please, start main_flask.py"
