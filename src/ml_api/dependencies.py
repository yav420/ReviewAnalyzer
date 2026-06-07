"""Зависимости FastAPI: создание классификатора (один раз на процесс)."""

from __future__ import annotations

from functools import lru_cache

from src.infrastructure.ml.classifier import SklearnSentimentClassifier


@lru_cache
def get_classifier() -> SklearnSentimentClassifier:
    """Загружает модель один раз и переиспользует (кэш)."""
    return SklearnSentimentClassifier()
