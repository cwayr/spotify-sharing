from flask import Flask
from flask_session import Session
from models import db, connect_db, User
from flask_login import LoginManager

from routes.landing_routes import landing_routes
from routes.user_routes import user_routes
from routes.group_routes import group_routes

app = Flask(__name__)

if app.config["ENV"] == "production":
    app.config.from_object('config.ProductionConfig')
elif app.config["ENV"] == "testing":
    app.config.from_object('config.TestingConfig')
else:
    app.config.from_object('config.DevelopmentConfig')

server_session = Session(app) # server-side session storage

login_manager = LoginManager()
login_manager.init_app(app)

connect_db(app)
db.create_all()

app.register_blueprint(landing_routes)
app.register_blueprint(user_routes)
app.register_blueprint(group_routes)

# flask login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
    