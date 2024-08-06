from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager
from dotenv import load_dotenv
from flask_mail import Mail
from flask_migrate import Migrate
import os

load_dotenv()

class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()
mail = Mail()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://blog_explore_user:NIiStc4BDsK4McPjKVhvI7rCQGXNPo0Y@dpg-cqooei2j1k6c73d5p4vg-a/blog_explore"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
    app.config['MAIL_SERVER'] = os.environ.get('SMTP_MAIL_SERVER')
    app.config['MAIL_PORT'] = os.environ.get('MAIL_PORT')
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

    mail.init_app(app)
    Bootstrap5(app=app)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    with app.app_context():
        from .models import User, BlogPost, Comment, Likes
        db.create_all()

    from .auth import auth
    app.register_blueprint(auth, url_prefix="/")

    from .views import views
    app.register_blueprint(views, url_prefix="/")

    return app
