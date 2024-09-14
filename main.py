from asyncio import run as run_async, set_event_loop_policy, WindowsSelectorEventLoopPolicy
from app.flask_web.main_flask import web


async def main():
    web.secret_key = 'db47bdf7d66e4b761ba5816edfb674930311faf4959b2999'
    await web.run(
        host="localhost",
        port=5000,
        debug=True,
    )


if __name__ == "__main__":
    set_event_loop_policy(WindowsSelectorEventLoopPolicy())
    run_async(main())
