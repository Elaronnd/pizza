from app.database.sqlite_pizza import sqlite
import asyncio
from app.flask_web import web


async def main():
    await web.run(
        host="localhost",
        port=5000,
        debug=True,
    )
    pizzas_class = await sqlite()
    if pizzas_class[0] is False:
        raise "something with sqlite"
    await pizzas_class[1].create_db()


if __name__ == "__main__":
    asyncio.run(main())
