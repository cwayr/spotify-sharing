from flask import Blueprint, render_template, redirect
from flask_login.utils import login_required
from models import db, User, Group, UserGroup

group_routes = Blueprint("group_routes", __name__, static_folder="../static", template_folder="../templates/group_page")


@group_routes.route("/user/<int:user_id>/group/<int:group_id>")
@login_required
def group_page(user_id, group_id):
    """Display group page."""

    user = User.query.get(user_id)
    group = Group.query.get(group_id)

    user_in_group = UserGroup.query.filter(UserGroup.user_id == user_id, UserGroup.group_id == group_id).first()
    print('user_in_group: ', user_in_group)

    return render_template("group.html", user=user, group=group, user_in_group=user_in_group)


@group_routes.route("/user/<int:user_id>/group/<int:group_id>/join", methods=["POST"])
@login_required
def add_user_to_group(user_id, group_id):
    """Add current user to group."""

    new_user_group = UserGroup(user_id=user_id, group_id=group_id)
    db.session.add(new_user_group)
    db.session.commit()

    return redirect(f"/user/{user_id}/group/{group_id}")


@group_routes.route("/user/<int:user_id>/group/<int:group_id>/leave", methods=["GET", "DELETE"])
@login_required
def remove_user_from_group(user_id, group_id):
    """Remove current user from group."""

    user_group = UserGroup.query.filter(UserGroup.user_id == user_id, UserGroup.group_id == group_id).first()
    db.session.delete(user_group)
    db.session.commit()

    return redirect(f"/user/{user_id}/group/{group_id}")