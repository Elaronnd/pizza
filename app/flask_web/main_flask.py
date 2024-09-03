from flask import Flask, render_template, request, redirect, url_for
from flask_httpauth import HTTPBasicAuth
from app.database.sqlite_pizza import sqlite
from app.debugs.change_logger import logger

web = Flask(__name__)
auth = HTTPBasicAuth()


@auth.verify_password
async def verify_pass(username: str, password: str):
    pizzas_class = await sqlite()
    check_username = await pizzas_class[1].check_username(username=username.lower())
    check_password = await pizzas_class[1].check_password(username=username.lower(), password=password.lower())
    if check_username[0] and check_password[0] is True:
        logger.debug("sqlite| someone login into admin page")
        return [True, username.lower()]


@web.route(rule="/", methods=["GET"])
async def index():
    pizzas_class = await sqlite()
    rows = await pizzas_class[1].check_all_table(table="list_pizzas")
    if rows[0] is False:
        return render_template(template_name_or_list="error.html", error="500"), 500
    for i in rows[1]:
        logger.debug(i)
    return render_template(template_name_or_list="index.html", rows=rows[1])


@web.route(rule="/pizza-order/",  methods=['GET'])
async def pizza_order():
    pizza_id = request.args.get("id")
    if pizza_id is None:
        return redirect(url_for("index")), 400
    pizzas_class = await sqlite()
    count_pizzas = await pizzas_class[1].check_count_pizzas(id=pizza_id)
    if count_pizzas[0] is False or int(count_pizzas[1]) <= 0:
        return redirect(url_for("index")), 403
    return render_template(template_name_or_list="order_pizza.html")


@web.route(rule="/admin", methods=["GET"])
@auth.login_required
async def admin():
    return render_template(template_name_or_list="admin.html")


@web.route(rule="/admin/view-pizzas", methods=["GET"])
@auth.login_required
async def view_pizzas():
    pizzas_class = await sqlite()
    info_pizzas = await pizzas_class[1].check_all_table(table="list_pizzas")
    return render_template(template_name_or_list="view_pizzas.html", data=info_pizzas[1])


@web.route(rule="/admin/view-orders", methods=["GET"])
@auth.login_required
async def view_orders():
    pizzas_class = await sqlite()
    info_pizzas = await pizzas_class[1].check_all_table(table="pizzas")
    return render_template(template_name_or_list="view_orders.html", data=info_pizzas[1])


@web.route(rule="/admin/edit-pizzas", methods=["GET", "POST"])
@auth.login_required
async def edit_pizzas():
    if request.method == "GET":
        return render_template(template_name_or_list="edit_pizzas.html")
    pizza_id = request.form["id"]
    pizza_name = request.form["name"]
    count_pizzas = request.form["count_pizzas"]
    pizza_price = request.form["price"]
    pizza_description = request.form["description"]
    pizzas_class = await sqlite()
    change_pizza = await pizzas_class[1].change_list_pizzas(id=pizza_id, name=pizza_name, count_pizzas=count_pizzas,
                                                            price=pizza_price, description=pizza_description)
    if change_pizza[0] is False:
        return redirect(url_for("edit_pizzas"))
    return redirect(url_for("admin"))


@web.route(rule="/admin/edit-orders", methods=["GET", "POST"])
@auth.login_required
async def edit_orders():
    if request.method == "GET":
        return render_template(template_name_or_list="edit_orders.html")
    order_id = request.form["id"]
    order_name = request.form["name"]
    order_phone_number = request.form["phone_number"]
    order_price = request.form["price"]
    order_complete_order = request.form["complete_order"]
    pizzas_class = await sqlite()
    change_pizza = await pizzas_class[1].change_pizzas(id=order_id, name=order_name, phone_number=order_phone_number,
                                                       price=order_price, complete_order=order_complete_order)
    if change_pizza[0] is False:
        return redirect(url_for("edit_orders"))
    return redirect(url_for("admin"))


@web.route(rule="/admin/delete-orders", methods=["GET", "POST"])
@auth.login_required
async def delete_orders():
    if request.method == "GET":
        return render_template(template_name_or_list="delete_orders.html")
    order_id = request.form["id"]
    pizzas_class = await sqlite()
    delete_pizza = await pizzas_class[1].delete_id_pizzas(id=order_id, table="pizzas")
    if delete_pizza[0] is False:
        return redirect(url_for("delete_orders"))
    return redirect(url_for("admin"))


@web.route(rule="/admin/delete_pizzas", methods=["GET", "POST"])
@auth.login_required
async def delete_pizzas():
    if request.method == "GET":
        return render_template(template_name_or_list="delete_pizzas.html")
    pizza_id = request.form["id"]
    pizzas_class = await sqlite()
    delete_pizza = await pizzas_class[1].delete_id_pizzas(id=pizza_id, table="list_pizzas")
    if delete_pizza[0] is False:
        return redirect(url_for("delete_pizzas"))
    return redirect(url_for("admin"))


@web.route(rule="/admin/add-orders", methods=["GET", "POST"])
@auth.login_required
async def add_orders():
    if request.method == "GET":
        return render_template(template_name_or_list="add_orders.html")
    order_id = request.form["id"]
    order_name = request.form["name"]
    order_phone_number = request.form["phone_number"]
    order_location = request.form["location"]
    order_complete_order = request.form["complete_order"]
    pizzas_class = await sqlite()
    delete_pizza = await pizzas_class[1].add_pizzas(id=order_id, name=order_name, phone_number=order_phone_number,
                                                    location=order_location, complete_order=order_complete_order)
    if delete_pizza[0] is False:
        return redirect(url_for("add_orders"))
    return redirect(url_for("admin"))


@web.route(rule="/admin/add-pizzas", methods=["GET", "POST"])
@auth.login_required
async def add_pizzas():
    if request.method == "GET":
        return render_template(template_name_or_list="add_pizzas.html")
    pizza_id = request.form["id"]
    pizza_name = request.form["name"]
    count_pizzas = request.form["count_pizzas"]
    pizza_price = request.form["price"]
    pizza_description = request.form["description"]
    pizzas_class = await sqlite()
    change_pizza = await pizzas_class[1].add_list_pizzas(id=pizza_id, name=pizza_name, count_pizzas=count_pizzas,
                                                            price=pizza_price, description=pizza_description)
    if change_pizza[0] is False:
        return redirect(url_for("add_pizzas"))
    return redirect(url_for("admin"))

if __name__ == "__main__":
    raise "Please, start main_flask.py"
