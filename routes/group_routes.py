from flask import Blueprint, render_template, redirect, session, request
from flask_login.utils import login_required
import requests
from urllib.parse import urlencode

from sqlalchemy.sql.functions import func
from forms import PostForm, GroupForm, SpotifySearchForm
from models import db, User, Group, UserGroup, Post, Likes
from flask_login import current_user
from spotify_api_auth import SpotifyAPI
from api_keys import CLIENT_ID, CLIENT_SECRET
from helpers import clear_session

group_routes = Blueprint("group_routes", __name__, static_folder="../static", template_folder="../templates/group_page")


@group_routes.route("/user/<int:user_id>/group/<int:group_id>", methods=["GET", "POST"])
@login_required
def group_page(user_id, group_id):
    """Display group page."""

    if user_id != current_user.id:
        return redirect(f'/user/{current_user.id}/group/{group_id}')

    user = User.query.get(user_id)
    group = Group.query.get(group_id)
    user_in_group = UserGroup.query.filter(UserGroup.user_id == user_id, UserGroup.group_id == group_id).first() # determine if user is in group (but not admin). Used to choose which action buttons to display.
    group_user_count = UserGroup.query.filter(UserGroup.group_id == group_id).count() # number of users in group

    posts = Post.query.filter(Post.group_id == group_id).all()
    top_recommended = Post.query.join(Likes).filter(Post.group_id == group_id, Post.s_name != None).group_by(Post.id).order_by(func.count().desc()).limit(5).all()

    post_form = PostForm()

    # remove selected song from session storage on button click
    if request.method == 'POST' and request.form["btn"] == "delete":
        clear_session()

    if not user_in_group:
        return render_template("group-unjoined.html", user=user, group=group, user_in_group=user_in_group, group_user_count=group_user_count, posts=posts, post_form=post_form, top_recommended=top_recommended, clear_session=clear_session)

    return render_template("group.html", user=user, group=group, user_in_group=user_in_group, group_user_count=group_user_count, posts=posts, post_form=post_form, top_recommended=top_recommended, clear_session=clear_session)


@group_routes.route("/user/<int:user_id>/group/<int:group_id>/post", methods=["POST"])
@login_required
def post(user_id, group_id):
    """Create post."""

    if user_id != current_user.id:
        return redirect(f'/user/{current_user.id}/group/{group_id}')

    post_form = PostForm()

    if post_form.validate_on_submit():
        content = post_form.content.data

        if session.get('track_name'):
            s_image=session.get('track_image')
            s_name=session.get('track_name')
            s_artist=session.get('track_artist')
            s_link=session.get('track_link')
            s_preview=session.get('track_preview')

            newPost = Post(content=content, user_id=user_id, group_id=group_id, s_image=s_image, s_name=s_name, s_artist=s_artist, s_link=s_link, s_preview=s_preview)

        else:
            newPost = Post(content=content, user_id=user_id, group_id=group_id)

        db.session.add(newPost)
        db.session.commit()
        clear_session()

        return redirect(f"/user/{user_id}/group/{group_id}")


@group_routes.route("/user/<int:user_id>/group/<int:group_id>/<int:post_id>/like", methods=["POST"])
@login_required
def like(user_id, group_id, post_id):
    """Like a post."""

    if user_id != current_user.id:
        return redirect(f'/user/{current_user.id}/group/{group_id}')

    user = User.query.get(user_id)
    post = Post.query.get(post_id)

    add_like = Likes(user_id=user.id, post_id=post.id)
    db.session.add(add_like)
    db.session.commit()

    return redirect(f"/user/{user_id}/group/{group_id}")


@group_routes.route("/user/<int:user_id>/group/<int:group_id>/<int:post_id>/unlike", methods=["GET", "DELETE"])
@login_required
def unlike(user_id, group_id, post_id):
    """Unlike a post."""

    if user_id != current_user.id:
        return redirect(f'/user/{current_user.id}/group/{group_id}')

    user = User.query.get(user_id)
    post = Post.query.get(post_id)

    post_like = Likes.query.filter(Likes.user_id == user.id, Likes.post_id == post.id).all()
    for like in post_like:
        db.session.delete(like)
        db.session.commit()

    return redirect(f"/user/{user_id}/group/{group_id}")


@group_routes.route("/user/<int:user_id>/group/<int:group_id>/<int:post_id>/delete", methods=["GET", "DELETE"])
@login_required
def delete_post(user_id, group_id, post_id):
    """Delete a post."""

    if user_id != current_user.id:
        return redirect(f'/user/{current_user.id}/group/{group_id}')

    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect(f"/user/{user_id}/group/{group_id}")


@group_routes.route("/user/<int:user_id>/group/<int:group_id>/join", methods=["POST"])
@login_required
def add_user_to_group(user_id, group_id):
    """Add current user to group."""

    if user_id != current_user.id:
        return redirect(f'/user/{current_user.id}/group/{group_id}')

    new_user_group = UserGroup(user_id=user_id, group_id=group_id)
    db.session.add(new_user_group)
    db.session.commit()

    return redirect(f"/user/{user_id}/group/{group_id}")


@group_routes.route("/user/<int:user_id>/group/<int:group_id>/leave", methods=["GET", "DELETE"])
@login_required
def remove_user_from_group(user_id, group_id):
    """Remove current user from group."""

    if user_id != current_user.id:
        return redirect(f'/user/{current_user.id}/group/{group_id}')

    user_group = UserGroup.query.filter(UserGroup.user_id == user_id, UserGroup.group_id == group_id).first()
    db.session.delete(user_group)
    db.session.commit()

    return redirect(f"/user/{user_id}/group/{group_id}")


@group_routes.route("/user/<int:user_id>/group/<int:group_id>/edit", methods=["GET", "POST"])
@login_required
def edit_group(user_id, group_id):
    """Edit group."""

    if user_id != current_user.id:
        return redirect(f'/user/{current_user.id}/group/{group_id}')

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

    if user_id != current_user.id:
        return redirect(f'/user/{current_user.id}/group/{group_id}')

    group = Group.query.get(group_id)
    db.session.delete(group)
    db.session.commit()

    return redirect(f"/user/{user_id}")


@group_routes.route("/user/<int:user_id>/group/<int:group_id>/search_spotify", methods=["GET", "POST"])
@login_required
def search_spotify(user_id, group_id):
    """Search Spotify API for songs."""

    if user_id != current_user.id:
        return redirect(f'/user/{current_user.id}/group/{group_id}/search_spotify')

    user = User.query.get(user_id)
    group = Group.query.get(group_id)

    search_form = SpotifySearchForm()

    # spotify search form
    if search_form.validate_on_submit() and request.form["btn"] == "search":
        query = search_form.query.data
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
        session["track_results"] = resp["tracks"]["items"]

    # add data from selected song to session
    if request.method == 'POST' and request.form["btn"] == "select":
        session['track_image'] = request.form.get('track_image')
        session['track_name'] = request.form.get('track_name')
        session['track_artist'] = request.form.get('track_artist')
        session['track_link'] = request.form.get('track_link')
        session['track_preview'] = request.form.get('track_preview')

        return redirect(f"/user/{user_id}/group/{group_id}")

    if (session.get('track_results') != None):
        return render_template("search_spotify.html", user=user, group=group, search_form=search_form, post_form=PostForm(), tracks=session.get('track_results'))
    else:
        return render_template("search_spotify.html", user=user, group=group, search_form=search_form, post_form=PostForm())