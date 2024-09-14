from flask import Flask, render_template, flash
from app.flask_web.admin_flask import admin_bp
from app.flask_web.user_flask import user_bp
import asyncio

web = Flask(__name__)
web.register_blueprint(admin_bp)
web.register_blueprint(user_bp)


@web.route(rule="/test")
async def test():
    flash("test")
    await asyncio.sleep(5)
    return render_template(template_name_or_list="base.html")

if __name__ == "__main__":
    raise "Please, start main.py"
