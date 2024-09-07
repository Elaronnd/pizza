from flask import Flask, render_template, request, redirect, url_for, make_response
from flask_httpauth import HTTPBasicAuth
from app.database.sqlite_pizza import sqlite
from app.debugs.change_logger import logger

web = Flask(__name__)
auth_admin = HTTPBasicAuth()


@auth_admin.verify_password
async def verify_pass_admin(username: str, password: str):
    pizzas_class = await sqlite()
    login_account = await pizzas_class[1].login_account(username=username, password=password)
    check_admin = await pizzas_class[1].check_admin(username=username.lower())
    if login_account[0] and check_admin[0] is True:
        logger.debug("sqlite| someone login into admin page")
        return [True, username.lower()]


@web.route(rule="/", methods=["GET"])
async def index():
    pizzas_class = await sqlite()
    rows = await pizzas_class[1].check_all_table(table="list_pizzas")
    if rows[0] is False:
        return render_template(template_name_or_list="error.html", error="500"), 500
    cookie_user = request.cookies.get("password")
    if cookie_user:
        return render_template(template_name_or_list="index.html", rows=rows[1], user=True)
    return render_template(template_name_or_list="index.html", rows=rows[1], login=True, register=True)


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
@auth_admin.login_required
async def admin():
    return render_template(template_name_or_list="admin.html")


@web.route(rule="/admin/view-pizzas", methods=["GET"])
@auth_admin.login_required
async def view_pizzas():
    pizzas_class = await sqlite()
    info_pizzas = await pizzas_class[1].check_all_table(table="list_pizzas")
    return render_template(template_name_or_list="view_pizzas.html", data=info_pizzas[1])


@web.route(rule="/admin/view-orders", methods=["GET"])
@auth_admin.login_required
async def view_orders():
    pizzas_class = await sqlite()
    info_pizzas = await pizzas_class[1].check_all_table(table="pizzas")
    return render_template(template_name_or_list="view_orders.html", data=info_pizzas[1])


@web.route(rule="/admin/edit-pizzas", methods=["GET", "POST"])
@auth_admin.login_required
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
@auth_admin.login_required
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
@auth_admin.login_required
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
@auth_admin.login_required
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
@auth_admin.login_required
async def add_orders():
    if request.method == "GET":
        return render_template(template_name_or_list="add_orders.html")
    order_id = request.form["id"]
    username = request.form["username"]
    order_name = request.form["name"]
    name_pizza = request.form["name_pizza"]
    order_phone_number = request.form["phone_number"]
    count = request.form["count"]
    price = request.form["price"]
    order_location = request.form["location"]
    order_complete_order = request.form["complete_order"]
    pizzas_class = await sqlite()
    add_pizza = await pizzas_class[1].order_pizza(id=order_id, username=username, name=order_name, name_pizza=name_pizza, phone_number=int(order_phone_number),
                                                    count=int(count), price=int(price), location=order_location, complete_order=bool(order_complete_order))
    if add_pizza[0] is False:
        logger.debug(f"teest/ {add_pizza}")
        return redirect(url_for("add_orders"))
    return redirect(url_for("admin"))


@web.route(rule="/admin/add-pizzas", methods=["GET", "POST"])
@auth_admin.login_required
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


@web.route(rule="/register", methods=["GET", "POST"])
async def register():
    cookie_user = request.cookies.get("password")
    if request.method == "GET" and cookie_user:
        return redirect(url_for(endpoint="index"))
    elif request.method == "GET":
        error = request.args.get("error")
        try:
            error.replace("+", " ")
        except AttributeError:
            pass
        return render_template(template_name_or_list="register.html", error=error, login=True)
    username = request.form["username"]
    password = request.form["password"]
    password_reply = request.form["password_reply"]
    if username and password and password_reply is None:
        return redirect(url_for(endpoint="register", error="Some parameters are none"))
    pizzas_class = await sqlite()
    create_account = await pizzas_class[1].create_account(username=username, password=password, reply_password=password_reply)
    if create_account[0] is False:
        return redirect(url_for(endpoint="register", error=create_account[1]))
    resp = make_response(redirect(url_for("index")))
    resp.set_cookie(key="password", value=create_account[1])
    return resp

@web.route(rule="/login", methods=["GET", "POST"])
async def login():
    cookie_user = request.cookies.get("password")
    if request.method == "GET" and cookie_user:
        return redirect(url_for(endpoint="index"))
    elif request.method == "GET":
        error = request.args.get("error")
        try:
            error.replace("+", " ")
        except AttributeError:
            pass
        return render_template(template_name_or_list="login.html", error=error, register=True)
    username = request.form["username"]
    password = request.form["password"]
    pizzas_class = await sqlite()
    login_account = await pizzas_class[1].login_account(username=username, password=password)
    if login_account[0] is False:
        return redirect(url_for(endpoint="login", error=login_account[1]))
    resp = make_response(redirect(url_for(endpoint="index")))
    resp.set_cookie(key="password", value=login_account[1])
    return resp


@web.route(rule="/profile")
async def profile():
    cookie_user = request.cookies.get("password")
    if not cookie_user:
        return redirect(url_for(endpoint="index"))
    pizzas_class = await sqlite()
    username = await pizzas_class[1].find_username(cookie=cookie_user)
    if username[0] is False:
        return render_template(template_name_or_list="error.html", error=500), 500
    users_orders = await pizzas_class[1].check_user_orders(username=username[1])
    logger.debug(f"test/ {users_orders} - orders")
    if users_orders[0] is False:
        return redirect(url_for("index"))
    return render_template(template_name_or_list="profile.html",
                           cookie=cookie_user,
                           username=username,
                           orders=users_orders[1],
                           len_orders=len(users_orders[1]))


@web.route(rule="/profile/logout")
async def logout():
    resp = make_response(redirect(url_for("index")))
    resp.delete_cookie(key="password")
    return resp


@web.route(rule="/profile/delete-account")
async def delete_account():
    cookie_user = request.cookies.get("password")
    if not cookie_user:
        return redirect(url_for(endpoint="index"))
    pizzas_class = await sqlite()
    result = await pizzas_class[1].delete_account(cookie=cookie_user)
    if result[0] is False:
        return render_template(template_name_or_list="error.html", error=500), 500
    resp = make_response(redirect(url_for("index")))
    resp.delete_cookie(key="password")
    return resp


@web.route(rule="/test")
async def test():
    return render_template(template_name_or_list="base.html")

if __name__ == "__main__":
    raise "Please, start main.py"
