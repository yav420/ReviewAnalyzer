"""Доменные сущности — «сердце» приложения.

Это обычные классы Python, описывающие бизнес-понятия.
Они НЕ знают ничего про базу данных, HTTP или фреймворки.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class User:
    """Пользователь системы."""

    username: str
    hashed_password: str
    id: int | None = None
    created_at: datetime | None = None


@dataclass
class Prediction:
    """Результат анализа тональности одного отзыва."""

    user_id: int
    input_data: str
    prediction: str
    id: int | None = None
    created_at: datetime | None = None


@dataclass
class SentimentResult:
    """Ответ ML-модели: метка тональности и уверенность."""

    label: str
    confidence: float
    probabilities: dict[str, float] = field(default_factory=dict)
