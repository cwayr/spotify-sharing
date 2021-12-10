from flask import Blueprint, render_template, redirect
from flask_login import login_required
from models import db, User, Group, UserGroup
from forms import NewGroupForm

user_routes = Blueprint("user_routes", __name__, static_folder="../static", template_folder="../templates/user_page")


@user_routes.route("/user/<int:user_id>")
@login_required
def user_page(user_id):
    """Home page for logged in user."""

    user = User.query.get(user_id)

    # groups a user has created
    created_groups = Group.query.filter_by(admin_id=user_id).all()

    # groups a user has joined
    users_groups = UserGroup.query.filter_by(user_id=user_id).all()
    joined_group_ids = [group.group_id for group in users_groups]
    joined_groups = Group.query.filter(Group.admin_id != user_id).filter(Group.id.in_(joined_group_ids)).all()

    return render_template("user-page.html", user=user, created_groups=created_groups, joined_groups=joined_groups)


@user_routes.route("/user/<int:user_id>/new-group", methods=["GET", "POST"])
@login_required
def create_new_group(user_id):
    """Create a new group."""

    user = User.query.get(user_id)
    form = NewGroupForm()

    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data

        new_group = Group(name=name, description=description, admin_id=user_id)
        db.session.add(new_group)
        db.session.commit()

        new_user_group = UserGroup(user_id=user_id, group_id=new_group.id)
        db.session.add(new_user_group)
        db.session.commit()

        return redirect(f"/user/{user_id}")

    return render_template("create-group.html", user=user, form=form)


@user_routes.route("/user/<int:user_id>/browse-groups")
@login_required
def browse_created_groups(user_id):
    """Browse all created groups."""

    user = User.query.get(user_id)

    joined_groups = UserGroup.query.filter_by(user_id=user_id).all()
    joined_group_ids = [group.group_id for group in joined_groups]
    groups = Group.query.filter(Group.admin_id != user_id).filter(Group.id.notin_(joined_group_ids)).all()

    return render_template("browse-groups.html", user=user, groups=groups)