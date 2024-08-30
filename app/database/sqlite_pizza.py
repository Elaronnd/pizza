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

            await self.connection.execute(
                'INSERT OR IGNORE INTO list_pizzas (id, name, count_pizzas, price, description) VALUES (0, "Margarita", 0, 300, "Піца “Маргарита” — це класична італійська піца, яка складається з простих, але дуже смачних інгредієнтів. Вона була створена в 1889 році неаполітанським піцайоло Рафаелем Еспозіто на честь королеви Італії Маргарити Савойської")')
            await self.connection.execute(
                'INSERT OR IGNORE INTO list_pizzas (id, name, count_pizzas, price, description) VALUES (1, "Pepperoni", 0, 250, "Піца “Пепероні” - це класична італійська піца, яка отримала свою назву від основного інгредієнта - ковбаси пепероні. Ця піца відрізняється своїм гострим і пікантним смаком, завдяки якому вона стала популярною у всьому світі.")')
            await self.connection.execute(
                'INSERT OR IGNORE INTO list_pizzas (id, name, count_pizzas, price, description) VALUES (2, "Four cheeses", 0, 300, "Чотири сири - різновид піци в італійській кухні, яка укомплектована комбінацією чотирьох видів сиру, зазвичай плавлених разом з томатним соусом.")')

        except aiosqlite.Error as error:
            logger.error(f"sqlite| sqlite got error in try block: {error}")
            return [False, error]
        return [True, "complete"]

    async def check_count_pizzas(self, id: int):
        try:
            await self.connection.execute('SELECT count_pizzas FROM list_pizzas WHERE id = ?', (id,))
            logger.debug(f"sqlite| execute in function \"check_count_pizzas\"\nid = {id}")
        except aiosqlite.Error as error:
            logger.error(f"sqlite| error in function \"check_count_pizzas\"\n error: {error}")
            return [False, error]
        else:
            logger.debug("sqlite| function \"check_count_pizzas\" was complete")
            result = await self.connection.fetchone()
            return [True, str(result[0])]

    async def add_count_pizzas(self, add_count: int, id: int):
        count_pizzas = await self.check_count_pizzas(id=id)
        if count_pizzas[0] is False:
            logger.error("sqlite| function \"add_count_pizzas\" got error, because function \"check_count_pizzas\" got error")
            return count_pizzas
        try:
            change_count_pizzas = int(count_pizzas[1]) + add_count
            await self.connection.execute('UPDATE list_pizzas SET count_pizzas = ? WHERE id = ?', (change_count_pizzas, id))
            logger.debug(f"sqlite| execute in function \"add_count_pizzas\"\ncount_pizzas = {change_count_pizzas}\nid = {id}")
            await self.connection.commit()
            logger.debug("sqlite| commit from function \"add_count_pizzas\"")
        except aiosqlite.Error as error:
            logger.error(f"sqlite| error in function \"add_count_pizzas\"\n error: {error}")
            return [False, error]
        else:
            logger.debug("sqlite| function \"add_count_pizzas\" was complete")
            return [True, str(add_count)]

    async def check_price_pizzas(self, id: int):
        try:
            await self.connection.execute('SELECT price FROM list_pizzas WHERE id = ?', (id,))
            logger.debug(f"sqlite| execute in function \"check_price_pizzas\"\nid = {id}")
        except aiosqlite.Error as error:
            logger.error(f"sqlite| error in function \"check_price_pizzas\"\n error: {error}")
            return [False, error]
        else:
            logger.debug("sqlite| function \"check_price_pizzas\" was complete")
            result = await self.connection.fetchone()
            return [True, str(result[0])]

    async def change_price_pizzas(self, price: int, id: int):
        price_pizza = await self.check_price_pizzas(id=id)
        if price_pizza[0] is False:
            logger.error("sqlite| function \"change_price_pizzas\" got error, because function \"check_price_pizzas\" got error")
            return price_pizza
        try:
            await self.connection.execute('UPDATE list_pizzas SET price = ? WHERE id = ?', (price, id))
            logger.debug(f"sqlite| execute in function \"change_price_pizzas\"\nprice = {price}\nid = {id}")
            await self.connection.commit()
            logger.debug("sqlite| commit from function \"change_price_pizzas\"")
        except aiosqlite.Error as error:
            logger.error(f"sqlite| error in function \"change_price_pizzas\"\n error: {error}")
            return [False, error]
        else:
            logger.debug("sqlite| function \"check_price_pizzas\" was complete")
            return [True, str(price)]

    async def remove_count_pizzas(self, remove_count: int, id: int):
        count_pizzas = await self.check_count_pizzas(id=id)
        if count_pizzas[0] is False:
            logger.error("sqlite| function \"change_price_pizzas\" got error, because function \"check_price_pizzas\" got error")
            return count_pizzas
        try:
            change_count_pizzas = int(count_pizzas[1]) - remove_count
            await self.connection.execute('UPDATE list_pizzas SET count_pizzas = ? WHERE id = ?',
                                (change_count_pizzas, id))
            logger.debug(f"sqlite| execute in function \"remove_count_pizzas\"\ncount_pizzas = {change_count_pizzas}\nid = {id}")
            await self.connection.commit()
            logger.debug("sqlite| commit from funtion \"remove_count_pizzas\"")
        except aiosqlite.Error as error:
            logger.error(f"sqlite| error in function \"remove_count_pizzas\"\n error: {error}")
            return [False, error]
        else:
            logger.debug("sqlite| function \"remove_count_pizzas\" was complete")
            return [True, str(remove_count)]

    async def order_pizza(self, id: int, name: str, phone_number: int):
        count_pizzas = await self.check_count_pizzas(id=id)
        if count_pizzas[0] is False:
            logger.error("sqlite| function \"order_pizza\" got error, because function \"check_count_pizzas\" got error")
            return count_pizzas
        elif count_pizzas[1] <= 0:
            error = "number of pizzas in stock - 0"
            logger.error(f"sqlite| function \"order_pizza\" got error, because {error}")
            return [False, error]
        try:
            order_date = datetime.strptime(str(datetime.now())[0:19], "%Y-%m-%d %H:%M:%S")
            await self.connection.execute(
                '''INSERT INTO pizzas (id, name, phone_number, order_date, complete_order) VALUES (?, ?, ?, ?, ?)''',
                (id, name, phone_number, order_date, 0)
            )
            logger.debug(f"sqlite| execute in function \"order_pizza\"\nid = {id}\nname = {name}\nphone_number = {phone_number}\norder_date = {order_date}")
            await self.connection.commit()
            logger.debug("sqlite| commit from function \"order_pizza\"")
        except aiosqlite.Error as error:
            logger.error(f"sqlite| error in function \"order_pizza\"\n error: {error}")
            return [False, error]
        remove_pizzas = await self.remove_count_pizzas(remove_count=1, id=id)
        if remove_pizzas is False:
            logger.error("sqlite| function \"order_pizza\" got error, because function \"remove_count_pizzas\" got error")
        else:
            logger.debug("sqlite| function \"order_pizza\" was complete")
        return remove_pizzas[0]

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
            await self.connection.execute(f"SELECT * FROM {table}")
            logger.debug(f"sqlite| execute in function \"check_all_pizza\"\ntable = {table}")
        except aiosqlite.Error as error:
            logger.error(f"sqlite| error in function \"check_all_pizza\"\n error: {error}")
            return [False, error]
        rows = await self.connection.fetchall()
        logger.debug("sqlite| function \"check_all_table\" was complete")
        return [True, rows]


async def sqlite():
    try:
        sqlite_connection = await aiosqlite.connect(database="app\\database\\pizza_python.db", timeout=30, check_same_thread=False)
        logger.debug("sqlite| connected to sqlite database")
    except aiosqlite.Error as error:
        logger.error(f"sqlite| error in function \"sqlite\"\n error: {error}")
        return [False, error]
    pizzas_class = Pizzas_Sqlite(connection=sqlite_connection)
    logger.debug("sqlite| function \"sqlite\" was complete")
    return [True, pizzas_class]


if __name__ == "__main__":
    raise "Please, start main.py"
