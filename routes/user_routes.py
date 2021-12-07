from flask import Blueprint, render_template, redirect
from flask_login import login_required
from models import db, User, Group
from forms import NewGroupForm

user_routes = Blueprint("user_routes", __name__, static_folder="../static", template_folder="../templates/user_page")


@user_routes.route("/user/<int:user_id>")
@login_required
def user_page(user_id):
    """Home page for logged in user."""

    user = User.query.get(user_id)

    return render_template("user-page.html", user=user)


@user_routes.route("/user/<int:user_id>/group", methods=["GET", "POST"])
@login_required
def create_new_group(user_id):
    """Create a new group."""

    user = User.query.get(user_id)
    form = NewGroupForm()

    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data

        newGroup = Group(name=name, description=description, admin_id=user_id)
        db.session.add(newGroup)
        db.session.commit()

        return redirect(f"/user/{user_id}")

    return render_template("create-group.html", user=user, form=form)