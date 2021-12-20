from flask import Blueprint, render_template, redirect, session
from flask_login.utils import login_required
import requests
from urllib.parse import urlencode
from forms import PostForm, GroupForm, SpotifySearchForm
from models import db, User, Group, UserGroup, Post
from spotify_api_auth import SpotifyAPI
from api_keys import CLIENT_ID, CLIENT_SECRET

group_routes = Blueprint("group_routes", __name__, static_folder="../static", template_folder="../templates/group_page")


@group_routes.route("/user/<int:user_id>/group/<int:group_id>", methods=["GET", "POST"])
@login_required
def group_page(user_id, group_id):
    """Display group page."""

    user = User.query.get(user_id)
    group = Group.query.get(group_id)
    user_in_group = UserGroup.query.filter(UserGroup.user_id == user_id, UserGroup.group_id == group_id).first() # determine if user is in group (but not admin). Used to choose which action buttons to display.
    posts = Post.query.filter(Post.group_id == group_id).all()

    form = PostForm()

    if form.validate_on_submit():
        content = form.content.data
        newPost = Post(content=content, user_id=user_id, group_id=group_id)
        db.session.add(newPost)
        db.session.commit()

        return redirect(f"/user/{user_id}/group/{group_id}")

    return render_template("group.html", user=user, group=group, user_in_group=user_in_group, posts=posts, form=form)


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


@group_routes.route("/user/<int:user_id>/group/<int:group_id>/edit", methods=["GET", "POST"])
@login_required
def edit_group(user_id, group_id):
    """Edit group."""

    user = User.query.get(user_id)
    group = Group.query.get(group_id)
    form = GroupForm(obj=group)

    if form.validate_on_submit():
        group.name = form.name.data
        group.description = form.description.data
        db.session.commit()

        return redirect(f"/user/{user_id}/group/{group_id}")

    return render_template("edit-group.html", user=user, group=group, form=form)


@group_routes.route("/user/<int:user_id>/group/<int:group_id>/delete", methods=["GET", "DELETE"])
@login_required
def delete_group(user_id, group_id):
    """Delete group."""

    group = Group.query.get(group_id)
    db.session.delete(group)
    db.session.commit()

    return redirect(f"/user/{user_id}")


@group_routes.route("/user/<int:user_id>/group/<int:group_id>/search_spotify", methods=["GET", "POST"])
@login_required
def search_spotify(user_id, group_id):

    user = User.query.get(user_id)
    group = Group.query.get(group_id)

    form = SpotifySearchForm()

    if form.validate_on_submit():
        query = form.query.data
        client = SpotifyAPI(CLIENT_ID, CLIENT_SECRET)
        client.authorize()
        token = client.access_token

        # run request
        headers = {"Authorization": f"Bearer {token}"}
        url = "https://api.spotify.com/v1/search"
        data = urlencode({"q": query, "type": "track"})
        lookup_url = f"{url}?{data}"

        r = requests.get(lookup_url, headers=headers)
        resp = r.json()
        session['track_results'] = resp["tracks"]["items"]

    if (session.get('track_results') != None):
        return render_template("search_spotify.html", user=user, group=group, form=form, tracks=session.get('track_results'))
    else:
        return render_template("search_spotify.html", user=user, group=group, form=form)