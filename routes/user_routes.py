from flask import Blueprint, render_template
from flask_login import login_required
from models import User

user_routes = Blueprint("user_routes", __name__, static_folder="../static", template_folder="../templates/user_page")


@user_routes.route("/user/<int:user_id>")
@login_required
def user_page(user_id):
    """Home page for logged in user."""

    user = User.query.get(user_id)

    return render_template("user-page.html", user=user)
