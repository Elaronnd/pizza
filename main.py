from asyncio import run as run_async
from app.flask_web.main_flask import web


async def main():
    await web.run(
        host="localhost",
        port=5000,
        debug=True,
    )


if __name__ == "__main__":
    run_async(main())
