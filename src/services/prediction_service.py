"""Сервис предсказаний: получить тональность и сохранить в историю.

Оркестрирует классификатор (ML) и репозиторий истории. Зависит только
от абстракций SentimentClassifier и PredictionRepository.
"""

from __future__ import annotations

from src.domain.entities import Prediction, SentimentResult
from src.domain.protocols import PredictionRepository, SentimentClassifier


class PredictionService:
    """Use-cases анализа тональности."""

    def __init__(
        self,
        classifier: SentimentClassifier,
        predictions: PredictionRepository,
    ) -> None:
        self._classifier = classifier
        self._predictions = predictions

    def analyze(self, user_id: int, text: str) -> SentimentResult:
        """Проанализировать текст и сохранить результат в историю."""
        result = self._classifier.predict(text)
        self._predictions.add(Prediction(user_id=user_id, input_data=text, prediction=result.label))
        return result

    def history(self, user_id: int) -> list[Prediction]:
        """Вернуть историю запросов пользователя."""
        return self._predictions.list_by_user(user_id)
