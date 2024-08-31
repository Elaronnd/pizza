import aiosqlite
from datetime import datetime
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

            await self.connection.commit()

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

            await self.connection.commit()

        except aiosqlite.Error as error:
            logger.error(f"sqlite| Error in create_db: {error}")
            return [False, error]
        logger.debug("sqlite| create_db was successful")
        return [True, "complete"]

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

    async def add_count_pizzas(self, add_count: int, id: int):
        count_pizzas = await self.check_count_pizzas(id=id)
        if not count_pizzas[0]:
            logger.error("sqlite| Error in add_count_pizzas: check_count_pizzas failed")
            return count_pizzas
        try:
            change_count_pizzas = int(count_pizzas[1]) + add_count
            await self.connection.execute('UPDATE list_pizzas SET count_pizzas = ? WHERE id = ?', (change_count_pizzas, id))
            await self.connection.commit()
        except aiosqlite.Error as error:
            logger.error(f"sqlite| Error in add_count_pizzas: {error}")
            return [False, error]
        logger.debug(f"sqlite| add_count_pizzas completed successfully: {change_count_pizzas}")
        return [True, str(add_count)]

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
                (id, name, phone_number, order_date, 0)
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
            await self.connection.execute('UPDATE pizzas SET complete_order = ? WHERE id = ?', (1, id))
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


async def sqlite():
    try:
        sqlite_connection = await aiosqlite.connect(database="app\\database\\pizza_python.db", timeout=30, check_same_thread=False)
        logger.debug("sqlite| connected to sqlite database")
        pizzas_class = Pizzas_Sqlite(connection=sqlite_connection)
        await pizzas_class.create_db()
    except aiosqlite.Error as error:
        logger.error(f"sqlite| error in function \"sqlite\"\n error: {error}")
        return [False, error]
    logger.debug("sqlite| function \"sqlite\" was complete")
    return [True, pizzas_class]


if __name__ == "__main__":
    raise "Please, start __init__.py"
