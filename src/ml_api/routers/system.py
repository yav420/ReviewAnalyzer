"""Системный роутер ML API: health и model-info."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from src.infrastructure.ml.classifier import SklearnSentimentClassifier
from src.ml_api.dependencies import get_classifier
from src.ml_api.schemas import HealthResponse, ModelInfoResponse

router = APIRouter(tags=["system"])


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    """Проверка работоспособности сервиса."""
    return HealthResponse(status="ok")


@router.get("/model-info", response_model=ModelInfoResponse)
def model_info(
    classifier: Annotated[SklearnSentimentClassifier, Depends(get_classifier)],
) -> ModelInfoResponse:
    """Информация о загруженной модели."""
    return ModelInfoResponse(
        name=classifier.name,
        version=classifier.version,
        classes=classifier.classes,
        feature_type="text",
    )
