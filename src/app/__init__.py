from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import getenv
from app.models import db
from app.models import Users
from .auth.routes import auth_bp
from .profile.routes import profile_bp

app = Flask(__name__)

# Load configuration from config.py or environment variables
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://{user}:{pw}@{url}/{db}'.format(
    user=getenv('DATABASE_USER'),
    pw=getenv('DATABASE_PASSWORD'),
    url=getenv('DATABASE_URL'),
    db=getenv('DATABASE_NAME')
)
app.config["SECRET_KEY"] = getenv('FLASK_SECRET_KEY')

login_manager = LoginManager()
login_manager.init_app(app)
db.init_app(app)

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(profile_bp)

# Home route
@app.route('/')
def home():
    return render_template('home.html')