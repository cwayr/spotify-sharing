from flask import Blueprint, render_template, redirect
from flask_login import login_user, logout_user
from forms import LoginForm, RegisterForm
from models import db, User
from helpers import clear_session

landing_routes = Blueprint("landing_routes", __name__, static_folder="../static", template_folder="../templates/landing_page")


@landing_routes.route("/")
def home():

    return redirect("/login")


@landing_routes.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.user_login(username, password)

        if user:
            login_user(user)
            return redirect(f"/user/{user.id}")
        else:
            form.username.errors = ["Incorrect username or password."]

    return render_template("login.html", form=form)


@landing_routes.route("/signup", methods=["GET", "POST"])
def signup():
    """Handle user signup."""

    form = RegisterForm()

    if form.validate_on_submit():
        name = form.name.data
        username = form.username.data
        password = form.password.data

        username_availibility = User.query.filter_by(username=form.username.data).first()

        if username_availibility:
            form.username.errors = ["Username already taken."]
            return render_template("signup.html", form=form)
        else:
            newUser = User.user_signup(name, username, password)
            db.session.add(newUser)
            db.session.commit()

            login_user(newUser)
            return redirect(f"/user/{newUser.id}")

    return render_template("signup.html", form=form)


@landing_routes.route("/logout")
def logout():
    """Handle logout."""

    logout_user()
    clear_session() # removes post draft data

    return redirect("/login")