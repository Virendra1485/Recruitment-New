from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    login_manager.init_app(app)

    from src.candidate.routes import candidate
    from src.admin.routes import admin

    app.register_blueprint(candidate)
    app.register_blueprint(admin)
    with app.app_context():
        db.create_all()

    CORS(app)
    return app
