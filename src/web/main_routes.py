"""Блюпринт основной логики: главная, анализ отзыва, история запросов."""

from __future__ import annotations

from flask import Blueprint, flash, render_template
from werkzeug import Response

from src.domain.entities import Prediction
from src.infrastructure.db.repositories import SqlPredictionRepository
from src.infrastructure.db.session import get_session
from src.web.extensions import current_user_id, login_required
from src.web.forms import AnalyzeForm
from src.web.ml_client import MLApiClient, MLApiError

bp = Blueprint("main", __name__)


@bp.route("/")
@login_required
def index() -> Response | str:
    """Главная страница с формой анализа."""
    return render_template("index.html", form=AnalyzeForm(), result=None)


@bp.route("/analyze", methods=["POST"])
@login_required
def analyze() -> Response | str:
    """Принимает отзыв, запрашивает ML API, сохраняет результат в историю."""
    form = AnalyzeForm()
    if not form.validate_on_submit():
        flash("Введите корректный текст отзыва", "warning")
        return render_template("index.html", form=form, result=None)

    text = form.text.data or ""
    client = MLApiClient()
    try:
        result = client.analyze(text)
    except MLApiError:
        flash("ML-сервис временно недоступен, попробуйте позже", "danger")
        return render_template("index.html", form=form, result=None)

    user_id = current_user_id()
    if user_id is not None:
        with get_session() as db:
            repo = SqlPredictionRepository(db)
            repo.add(Prediction(user_id=user_id, input_data=text, prediction=result.label))

    return render_template("index.html", form=AnalyzeForm(), result=result, analyzed_text=text)


@bp.route("/history")
@login_required
def history() -> Response | str:
    """Страница истории запросов пользователя."""
    user_id = current_user_id()
    items: list[Prediction] = []
    if user_id is not None:
        with get_session() as db:
            repo = SqlPredictionRepository(db)
            items = repo.list_by_user(user_id)
    return render_template("history.html", items=items)


@bp.route("/healthz")
def healthz() -> tuple[str, int]:
    """Healthcheck Flask-приложения (для docker-compose)."""
    return "ok", 200
