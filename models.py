from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """User for the app."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)


class Group(db.Model):
    """Group page."""

    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class UserGroup(db.Model):
    """Maps users to their groups."""

    __tablename__ = 'user_groups'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))


class Post(db.Model):
    """User posts."""

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
    content = db.Column(db.String)
    spotify_id = db.Column(db.String)
    is_reply = db.Column(db.Boolean, default=False)
    reply_to = db.Column(db.Integer, db.ForeignKey('posts.id'))


def connect_db(app):
    """Connect this database to Flask app."""

    db.app = app
    db.init_app(app)