"""Роутер предсказаний ML API."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from src.infrastructure.ml.classifier import SklearnSentimentClassifier
from src.ml_api.dependencies import get_classifier
from src.ml_api.schemas import PredictRequest, PredictResponse

router = APIRouter(tags=["prediction"])


@router.post("/predict", response_model=PredictResponse)
def predict(
    payload: PredictRequest,
    classifier: Annotated[SklearnSentimentClassifier, Depends(get_classifier)],
) -> PredictResponse:
    """Принимает текст отзыва, возвращает тональность и уверенность."""
    result = classifier.predict(payload.text)
    return PredictResponse(
        label=result.label,
        confidence=result.confidence,
        probabilities=result.probabilities,
    )
