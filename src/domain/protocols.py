"""Протоколы (контракты) для внешних зависимостей.

Внутренние слои (services, domain) зависят от ЭТИХ абстракций,
а не от конкретных реализаций. Конкретные репозитории (PostgreSQL)
и классификатор (sklearn) живут в слое infrastructure и обязаны
соответствовать этим протоколам.

Это и есть принцип инверсии зависимостей: направление зависимости
указывает внутрь, к домену.
"""

from __future__ import annotations

from typing import Protocol

from src.domain.entities import Prediction, SentimentResult, User


class UserRepository(Protocol):
    """Контракт хранилища пользователей."""

    def add(self, user: User) -> User:
        """Сохранить нового пользователя, вернуть его с присвоенным id."""
        ...

    def get_by_username(self, username: str) -> User | None:
        """Найти пользователя по логину или вернуть None."""
        ...

    def get_by_id(self, user_id: int) -> User | None:
        """Найти пользователя по id или вернуть None."""
        ...


class PredictionRepository(Protocol):
    """Контракт хранилища истории предсказаний."""

    def add(self, prediction: Prediction) -> Prediction:
        """Сохранить предсказание, вернуть его с присвоенным id."""
        ...

    def list_by_user(self, user_id: int) -> list[Prediction]:
        """Вернуть все предсказания пользователя (новые сверху)."""
        ...


class SentimentClassifier(Protocol):
    """Контракт модели анализа тональности."""

    def predict(self, text: str) -> SentimentResult:
        """Определить тональность текста."""
        ...

    @property
    def name(self) -> str:
        """Название модели."""
        ...

    @property
    def version(self) -> str:
        """Версия модели."""
        ...

    @property
    def classes(self) -> list[str]:
        """Список возможных меток."""
        ...
