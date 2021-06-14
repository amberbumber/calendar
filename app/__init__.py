# -*- coding: utf-8 -*-
from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap


# инициализация объектов
bootstrap = Bootstrap()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    bootstrap.init_app(app)

    # регистрация схемы данных в приложении
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app