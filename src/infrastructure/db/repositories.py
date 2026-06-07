"""Реализации репозиториев на SQLAlchemy (синхронные, для Flask).

Соответствуют протоколам из src.domain.protocols. Преобразуют
доменные сущности в ORM-модели и обратно.
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.domain.entities import Prediction, User
from src.infrastructure.db.models import PredictionModel, UserModel


class SqlUserRepository:
    """Хранилище пользователей поверх SQLAlchemy."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, user: User) -> User:
        model = UserModel(username=user.username, hashed_password=user.hashed_password)
        self._session.add(model)
        self._session.flush()
        return self._to_entity(model)

    def get_by_username(self, username: str) -> User | None:
        stmt = select(UserModel).where(UserModel.username == username)
        model = self._session.scalar(stmt)
        return self._to_entity(model) if model else None

    def get_by_id(self, user_id: int) -> User | None:
        model = self._session.get(UserModel, user_id)
        return self._to_entity(model) if model else None

    @staticmethod
    def _to_entity(model: UserModel) -> User:
        return User(
            id=model.id,
            username=model.username,
            hashed_password=model.hashed_password,
            created_at=model.created_at,
        )


class SqlPredictionRepository:
    """Хранилище истории предсказаний поверх SQLAlchemy."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, prediction: Prediction) -> Prediction:
        model = PredictionModel(
            user_id=prediction.user_id,
            input_data=prediction.input_data,
            prediction=prediction.prediction,
        )
        self._session.add(model)
        self._session.flush()
        return self._to_entity(model)

    def list_by_user(self, user_id: int) -> list[Prediction]:
        stmt = (
            select(PredictionModel)
            .where(PredictionModel.user_id == user_id)
            .order_by(PredictionModel.created_at.desc())
        )
        return [self._to_entity(m) for m in self._session.scalars(stmt).all()]

    @staticmethod
    def _to_entity(model: PredictionModel) -> Prediction:
        return Prediction(
            id=model.id,
            user_id=model.user_id,
            input_data=model.input_data,
            prediction=model.prediction,
            created_at=model.created_at,
        )
