"""Сервис аутентификации: регистрация и проверка пользователей.

Зависит только от абстракции UserRepository (внедряется через конструктор),
а не от конкретной БД. Пароли хешируются (werkzeug).
"""

from __future__ import annotations

from werkzeug.security import check_password_hash, generate_password_hash

from src.domain.entities import User
from src.domain.protocols import UserRepository


class UserAlreadyExistsError(Exception):
    """Пользователь с таким логином уже зарегистрирован."""


class InvalidCredentialsError(Exception):
    """Неверный логин или пароль."""


class AuthService:
    """Use-cases аутентификации."""

    def __init__(self, users: UserRepository) -> None:
        self._users = users

    def register(self, username: str, password: str) -> User:
        if self._users.get_by_username(username) is not None:
            raise UserAlreadyExistsError(username)
        user = User(username=username, hashed_password=generate_password_hash(password))
        return self._users.add(user)

    def authenticate(self, username: str, password: str) -> User:
        user = self._users.get_by_username(username)
        if user is None or not check_password_hash(user.hashed_password, password):
            raise InvalidCredentialsError(username)
        return user
