from flask import Flask, render_template, request, redirect, url_for, make_response, Blueprint
from app.database.sqlite_pizza import sqlite
from app.flask_web.admin_flask import admin_bp

web = Flask(__name__)
web.register_blueprint(admin_bp)


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
    elif username != password_reply:
        redirect(url_for(endpoint="register", error="Reply password is not password"))
    pizzas_class = await sqlite()
    create_account = await pizzas_class[1].create_account(username=username, password=password)
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
