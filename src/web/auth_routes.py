"""Блюпринт аутентификации: регистрация, вход, выход."""

from __future__ import annotations

from flask import Blueprint, flash, redirect, render_template, session, url_for
from werkzeug import Response

from src.infrastructure.db.repositories import SqlUserRepository
from src.infrastructure.db.session import get_session
from src.services.auth_service import (
    AuthService,
    InvalidCredentialsError,
    UserAlreadyExistsError,
)
from src.web.extensions import current_user_id
from src.web.forms import LoginForm, RegisterForm

bp = Blueprint("auth", __name__)


@bp.route("/register", methods=["GET", "POST"])
def register() -> Response | str:
    """Регистрация нового пользователя."""
    if current_user_id() is not None:
        return redirect(url_for("main.index"))

    form = RegisterForm()
    if form.validate_on_submit():
        with get_session() as db:
            service = AuthService(SqlUserRepository(db))
            try:
                service.register(form.username.data or "", form.password.data or "")
            except UserAlreadyExistsError:
                flash("Пользователь с таким логином уже существует", "danger")
                return render_template("register.html", form=form)
        flash("Регистрация успешна, теперь войдите", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html", form=form)


@bp.route("/login", methods=["GET", "POST"])
def login() -> Response | str:
    """Вход в систему."""
    if current_user_id() is not None:
        return redirect(url_for("main.index"))

    form = LoginForm()
    if form.validate_on_submit():
        with get_session() as db:
            service = AuthService(SqlUserRepository(db))
            try:
                user = service.authenticate(form.username.data or "", form.password.data or "")
            except InvalidCredentialsError:
                flash("Неверный логин или пароль", "danger")
                return render_template("login.html", form=form)
            session["user_id"] = user.id
            session["username"] = user.username
        flash("Вы вошли в систему", "success")
        return redirect(url_for("main.index"))

    return render_template("login.html", form=form)


@bp.route("/logout")
def logout() -> Response:
    """Выход из системы."""
    session.clear()
    flash("Вы вышли из системы", "info")
    return redirect(url_for("auth.login"))
