from flask import Blueprint, render_template
from flask_login.utils import login_required
from models import User, Group

group_routes = Blueprint("group_routes", __name__, static_folder="../static", template_folder="../templates/group_page")


@group_routes.route("/user/<int:user_id>/group/<int:group_id>")
@login_required
def group_page(user_id, group_id):

    user = User.query.get(user_id)
    group = Group.query.get(group_id)

    return render_template("group.html", user=user, group=group)