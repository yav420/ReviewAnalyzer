"""Pydantic-схемы для валидации запросов и ответов ML API."""

from __future__ import annotations

from pydantic import BaseModel, Field


class PredictRequest(BaseModel):
    """Входные данные для предсказания."""

    text: str = Field(min_length=1, max_length=5000, description="Текст отзыва")


class PredictResponse(BaseModel):
    """Результат предсказания."""

    label: str
    confidence: float
    probabilities: dict[str, float]


class HealthResponse(BaseModel):
    """Ответ healthcheck."""

    status: str


class ModelInfoResponse(BaseModel):
    """Информация о модели."""

    name: str
    version: str
    classes: list[str]
    feature_type: str
