"""Модульные тесты сервиса аутентификации."""

from __future__ import annotations

import pytest
from src.services.auth_service import (
    AuthService,
    InvalidCredentialsError,
    UserAlreadyExistsError,
)

from tests.fakes import FakeUserRepository


def test_register_creates_user_with_hashed_password() -> None:
    service = AuthService(FakeUserRepository())
    user = service.register("alice", "secret123")
    assert user.id is not None
    assert user.username == "alice"
    # Пароль не хранится в открытом виде
    assert user.hashed_password != "secret123"


def test_register_duplicate_username_raises() -> None:
    repo = FakeUserRepository()
    service = AuthService(repo)
    service.register("bob", "pass")
    with pytest.raises(UserAlreadyExistsError):
        service.register("bob", "another")


def test_authenticate_with_correct_password() -> None:
    service = AuthService(FakeUserRepository())
    service.register("carol", "mypassword")
    user = service.authenticate("carol", "mypassword")
    assert user.username == "carol"


def test_authenticate_with_wrong_password_raises() -> None:
    service = AuthService(FakeUserRepository())
    service.register("dave", "rightpass")
    with pytest.raises(InvalidCredentialsError):
        service.authenticate("dave", "wrongpass")


def test_authenticate_unknown_user_raises() -> None:
    service = AuthService(FakeUserRepository())
    with pytest.raises(InvalidCredentialsError):
        service.authenticate("ghost", "whatever")
