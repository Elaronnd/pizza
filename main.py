import asyncio
from app.flask_web import web


async def main():
    await web.run(
        host="localhost",
        port=5000,
        debug=True,
    )


if __name__ == "__main__":
    asyncio.run(main())
