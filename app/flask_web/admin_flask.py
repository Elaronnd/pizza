from flask import redirect, render_template, request, url_for, Blueprint
from app.debugs.change_logger import logger
from app.database.sqlite_pizza import sqlite
from flask_httpauth import HTTPBasicAuth


auth_admin = HTTPBasicAuth()
admin_bp = Blueprint("admin", __name__)


@auth_admin.verify_password
async def verify_pass_admin(username: str, password: str):
    pizzas_class = await sqlite()
    login_account = await pizzas_class[1].login_account(username=username, password=password)
    check_admin = await pizzas_class[1].check_admin(username=username.lower())
    if login_account[0] and check_admin[0] is True:
        logger.debug("sqlite| someone login into admin page.")
        return [True, username.lower()]

@admin_bp.route(rule="/admin/delete-users", methods=["GET", "POST"])
@auth_admin.login_required
async def delete_users():
    if request.method == "GET":
        return render_template(template_name_or_list="delete.html", table="юзерів")
    user_id = request.form["id"]
    pizzas_class = await sqlite()
    delete_pizza = await pizzas_class[1].delete_by_id_table(id=user_id, table="users")
    if delete_pizza[0] is False:
        return redirect(url_for("delete_users"))
    return redirect(url_for("admin"))


@admin_bp.route(rule="/admin/add-orders", methods=["GET", "POST"])
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
        return redirect(url_for("add_orders"))
    return redirect(url_for("admin"))


@admin_bp.route(rule="/admin/add-pizzas", methods=["GET", "POST"])
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


@admin_bp.route(rule="/admin/add-users", methods=["GET", "POST"])
@auth_admin.login_required
async def add_users():
    if request.method == "GET":
        return render_template(template_name_or_list="add_users.html")
    username = request.form["username"]
    password = request.form["password"]
    admin_user = request.form["admin"]
    pizzas_class = await sqlite()
    add_user = await pizzas_class[1].create_account(username=username.lower(), password=password.lower(), admin=bool(admin_user))
    if add_user[0] is False:
        return redirect(url_for("add_users"))
    return redirect(url_for("admin"))

@admin_bp.route(rule="/admin", methods=["GET"])
@auth_admin.login_required
async def admin():
    return render_template(template_name_or_list="admin.html")


@admin_bp.route(rule="/admin/view-pizzas", methods=["GET"])
@auth_admin.login_required
async def view_pizzas():
    pizzas_class = await sqlite()
    info_pizzas = await pizzas_class[1].check_all_table(table="list_pizzas")
    return render_template(template_name_or_list="view_pizzas.html", data=info_pizzas[1])


@admin_bp.route(rule="/admin/view-orders", methods=["GET"])
@auth_admin.login_required
async def view_orders():
    pizzas_class = await sqlite()
    info_pizzas = await pizzas_class[1].check_all_table(table="pizzas")
    return render_template(template_name_or_list="view_orders.html", data=info_pizzas[1])


@admin_bp.route(rule="/admin/view-users")
@auth_admin.login_required
async def view_users():
    pizzas_class = await sqlite()
    info_pizzas = await pizzas_class[1].check_all_table(table="users")
    return render_template(template_name_or_list="view_users.html", data=info_pizzas[1])


@admin_bp.route(rule="/admin/edit-pizzas", methods=["GET", "POST"])
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


@admin_bp.route(rule="/admin/edit-orders", methods=["GET", "POST"])
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


@admin_bp.route(rule="/admin/edit-users", methods=["GET", "POST"])
@auth_admin.login_required
async def edit_users():
    if request.method == "GET":
        return render_template(template_name_or_list="edit_users.html")
    id_user = request.form["id"]
    username = request.form["username"]
    password = request.form["password"]
    admin_user = request.form["admin"]
    pizzas_class = await sqlite()
    edit_user = await pizzas_class[1].change_user(id=id_user, username=username.lower(), password=password.lower(), admin=bool(admin_user))
    if edit_user[0] is False:
        return redirect(url_for("edit_users"))
    return redirect(url_for("admin"))


@admin_bp.route(rule="/admin/delete-orders", methods=["GET", "POST"])
@auth_admin.login_required
async def delete_orders():
    if request.method == "GET":
        return render_template(template_name_or_list="delete.html", table="замовлення")
    order_id = request.form["id"]
    pizzas_class = await sqlite()
    delete_pizza = await pizzas_class[1].delete_by_id_table(id=order_id, table="pizzas")
    if delete_pizza[0] is False:
        return redirect(url_for("delete_orders"))
    return redirect(url_for("admin"))


@admin_bp.route(rule="/admin/delete-pizzas", methods=["GET", "POST"])
@auth_admin.login_required
async def delete_pizzas():
    if request.method == "GET":
        return render_template(template_name_or_list="delete.html", table="піц")
    pizza_id = request.form["id"]
    pizzas_class = await sqlite()
    delete_pizza = await pizzas_class[1].delete_by_id_table(id=pizza_id, table="list_pizzas")
    if delete_pizza[0] is False:
        return redirect(url_for("delete_pizzas"))
    return redirect(url_for("admin"))