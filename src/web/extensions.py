"""Расширения Flask и помощники авторизации.

Flask хранит состояние входа в сессии (server-side через подписанные cookie).
Декоратор login_required защищает страницы от неавторизованного доступа.
"""

from __future__ import annotations

from collections.abc import Callable
from functools import wraps
from typing import TypeVar

from flask import flash, redirect, session, url_for
from werkzeug import Response

F = TypeVar("F", bound=Callable[..., object])


def login_required(view: F) -> F:
    """Пускает на страницу только авторизованных пользователей."""

    @wraps(view)
    def wrapper(*args: object, **kwargs: object) -> object:
        if session.get("user_id") is None:
            flash("Сначала войдите в систему", "warning")
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)

    return wrapper  # type: ignore[return-value]


def current_user_id() -> int | None:
    """Возвращает id текущего пользователя из сессии (или None)."""
    user_id = session.get("user_id")
    return int(user_id) if user_id is not None else None


def redirect_to(endpoint: str) -> Response:
    """Типизированная обёртка над redirect(url_for(...))."""
    return redirect(url_for(endpoint))
