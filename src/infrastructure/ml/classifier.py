"""Реализация классификатора тональности на основе обученной модели.

Загружает model.pkl (pipeline + метаданные) и реализует протокол
SentimentClassifier из доменного слоя.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, cast

import joblib

from src.domain.entities import SentimentResult

DEFAULT_MODEL_PATH = Path(__file__).resolve().parents[3] / "ml" / "model.pkl"


class SklearnSentimentClassifier:
    """Классификатор тональности поверх sklearn-pipeline."""

    def __init__(self, model_path: Path | None = None) -> None:
        path = model_path or DEFAULT_MODEL_PATH
        artifact: dict[str, Any] = joblib.load(path)
        self._pipeline = artifact["pipeline"]
        self._name: str = artifact["name"]
        self._version: str = artifact["version"]
        self._classes: list[str] = artifact["classes"]

    def predict(self, text: str) -> SentimentResult:
        label = cast(str, self._pipeline.predict([text])[0])
        proba = self._pipeline.predict_proba([text])[0]
        probabilities = {
            cls: float(p) for cls, p in zip(self._pipeline.classes_, proba, strict=True)
        }
        confidence = max(probabilities.values())
        return SentimentResult(label=label, confidence=confidence, probabilities=probabilities)

    @property
    def name(self) -> str:
        return self._name

    @property
    def version(self) -> str:
        return self._version

    @property
    def classes(self) -> list[str]:
        return self._classes
