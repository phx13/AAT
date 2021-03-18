from flask import Flask
# from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
# login_manager = LoginManager()
# login_manager.login_view = 'login'


def create_app():
    app = Flask(__name__)

    from config import DevelopmentConfig
    app.config.from_object(DevelopmentConfig)

    db.init_app(app)
    # login_manager.init_app(app)

    from aat.main import bp as main_bp
    from aat.auth import bp as auth_bp
    from aat.errors import bp as error_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(error_bp)

    return app
