from flask import Flask, render_template
from app.database.sqlite_pizza import sqlite
from app.debugs.change_logger import logger

web = Flask(__name__)


@web.route("/")
async def index():
    pizzas_class = await sqlite()
    rows = await pizzas_class[1].check_all_table(table="list_pizzas")
    if rows[0] is False:
        return render_template(template_name_or_list="error.html", error="500"), 500
    for i in rows[1]:
        logger.debug(f"test| {i}")
    return render_template(template_name_or_list="index.html", rows=rows[1])


if __name__ == "__main__":
    raise "Please, start __init__.py"
