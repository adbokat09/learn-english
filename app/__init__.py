import os
from flask import Flask
from app.config.db import db


def create_app():
    app = Flask(__name__)

    base_path = os.path.dirname(os.path.dirname(__file__))
    app.config['SECRET_KEY'] = 'secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_path, 'english.sqlite')

    db.init_app(app)

    from app.auth.views import bp as auth_bp
    from app.user.views import bp as user_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)

    return app