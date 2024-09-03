import asyncio
from app.database.sqlite_pizza import sqlite
from app.flask_web.main_flask import web


async def main():
    await web.run(
        host="localhost",
        port=5000,
        debug=True,
    )
    pizzas_class = await sqlite()
    await pizzas_class[1].create_db()
    await pizzas_class[1].create_default()


if __name__ == "__main__":
    asyncio.run(main())
