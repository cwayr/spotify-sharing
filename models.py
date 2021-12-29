from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import backref

bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):
    """User for the app."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    introduction = db.Column(db.String(250))

    # the four following properties are for flask-login
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    @classmethod
    def user_signup(cls, name, username, password):
        """User registration using bcrypt for password encryption."""

        hashed_pw = bcrypt.generate_password_hash(password).decode('UTF-8')

        return cls(full_name=name, username=username, password=hashed_pw)

    @classmethod
    def user_login(cls, username, password):
        """User login, checks encrypted password."""

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False


class UserGroup(db.Model):
    """Maps users to their groups."""

    __tablename__ = 'users_groups'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id', ondelete='CASCADE'))


class Group(db.Model):
    """Group page."""

    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))

    user = db.relationship('User', backref=backref('groups', cascade='all, delete-orphan'))


class Post(db.Model):
    """User posts."""

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id', ondelete='CASCADE'))
    content = db.Column(db.String, nullable=False)
    s_image = db.Column(db.String)
    s_name = db.Column(db.String)
    s_artist = db.Column(db.String)
    s_link = db.Column(db.String)
    s_preview = db.Column(db.String)
    is_reply = db.Column(db.Boolean, default=False)
    reply_to = db.Column(db.Integer, db.ForeignKey('posts.id', ondelete='CASCADE'))

    user = db.relationship('User', backref=backref('posts', cascade='all, delete-orphan'))
    likes = db.relationship('Likes', backref=backref('posts', single_parent=True))


class Likes(db.Model):
    """User likes."""

    __tablename__ = 'likes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    __tableargs__ = (db.UniqueConstraint('user_id', 'post_id', name='_user_post_uc')) #https://stackoverflow.com/questions/10059345/sqlalchemy-unique-across-multiple-columns


def connect_db(app):
    """Connect this database to Flask app."""

    db.app = app
    db.init_app(app)