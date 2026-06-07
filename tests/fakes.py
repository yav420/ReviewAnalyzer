"""Фейковые реализации репозиториев и классификатора для тестов.

Позволяют тестировать сервисы без реальной БД и ML-модели,
подменяя зависимости через конструктор (инверсия зависимостей).
"""

from __future__ import annotations

from datetime import UTC, datetime

from src.domain.entities import Prediction, SentimentResult, User


class FakeUserRepository:
    """In-memory хранилище пользователей."""

    def __init__(self) -> None:
        self._users: dict[int, User] = {}
        self._next_id = 1

    def add(self, user: User) -> User:
        stored = User(
            id=self._next_id,
            username=user.username,
            hashed_password=user.hashed_password,
            created_at=datetime.now(UTC),
        )
        self._users[self._next_id] = stored
        self._next_id += 1
        return stored

    def get_by_username(self, username: str) -> User | None:
        for user in self._users.values():
            if user.username == username:
                return user
        return None

    def get_by_id(self, user_id: int) -> User | None:
        return self._users.get(user_id)


class FakePredictionRepository:
    """In-memory хранилище истории предсказаний."""

    def __init__(self) -> None:
        self._items: list[Prediction] = []
        self._next_id = 1

    def add(self, prediction: Prediction) -> Prediction:
        stored = Prediction(
            id=self._next_id,
            user_id=prediction.user_id,
            input_data=prediction.input_data,
            prediction=prediction.prediction,
            created_at=datetime.now(UTC),
        )
        self._items.append(stored)
        self._next_id += 1
        return stored

    def list_by_user(self, user_id: int) -> list[Prediction]:
        return [p for p in self._items if p.user_id == user_id]


class FakeClassifier:
    """Классификатор-заглушка: всегда возвращает фиксированный результат."""

    def predict(self, text: str) -> SentimentResult:
        return SentimentResult(
            label="positive",
            confidence=0.9,
            probabilities={"positive": 0.9, "negative": 0.05, "neutral": 0.05},
        )

    @property
    def name(self) -> str:
        return "fake-classifier"

    @property
    def version(self) -> str:
        return "0.0.1"

    @property
    def classes(self) -> list[str]:
        return ["negative", "neutral", "positive"]
