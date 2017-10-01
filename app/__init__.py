from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment

from config import config
from .models import flask_db

bootstrap = Bootstrap()
moment = Moment()


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    bootstrap.init_app(app)
    moment.init_app(app)

    # init database
    flask_db.init_app(app)

    # register blueprint
    from .main import main as main_bp
    from .auth import auth as auth_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app
