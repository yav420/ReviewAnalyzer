"""Точка входа веб-приложения (Flask).

Запуск в контейнере (через gunicorn или flask run):
    flask --app src.web.app run --host 0.0.0.0 --port 5000
"""

from __future__ import annotations

import sys

from flask import Flask
from flask_wtf import CSRFProtect
from loguru import logger

from src.config import get_settings
from src.web.auth_routes import bp as auth_bp
from src.web.main_routes import bp as main_bp

logger.remove()
logger.add(sys.stdout, level="INFO")
logger.add(sys.stderr, level="ERROR")

csrf = CSRFProtect()


def create_app() -> Flask:
    """Собирает и настраивает приложение Flask."""
    settings = get_settings()
    app = Flask(__name__)
    app.config["SECRET_KEY"] = settings.flask_secret_key
    app.config["WTF_CSRF_ENABLED"] = True

    csrf.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    logger.info("Flask-приложение инициализировано")
    return app


app = create_app()
