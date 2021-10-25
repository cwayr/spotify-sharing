from flask import Flask, render_template

app = Flask(__name__)

if app.config["ENV"] == "production":
    app.config.from_object('config.ProductionConfig')
elif app.config["ENV"] == "testing":
    app.config.from_object('config.TestingConfig')
else:
    app.config.from_object('config.developmentConfig')


@app.route('/', methods=['GET', 'POST'])
def home():

    """Handle user signup."""
    return render_template('base.html')