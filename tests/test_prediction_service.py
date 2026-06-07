"""Модульные тесты сервиса предсказаний."""

from __future__ import annotations

from src.services.prediction_service import PredictionService

from tests.fakes import FakeClassifier, FakePredictionRepository


def test_analyze_returns_classifier_result() -> None:
    service = PredictionService(FakeClassifier(), FakePredictionRepository())
    result = service.analyze(user_id=1, text="отличный товар")
    assert result.label == "positive"
    assert result.confidence == 0.9


def test_analyze_saves_prediction_to_history() -> None:
    repo = FakePredictionRepository()
    service = PredictionService(FakeClassifier(), repo)
    service.analyze(user_id=42, text="хороший отзыв")
    history = service.history(user_id=42)
    assert len(history) == 1
    assert history[0].input_data == "хороший отзыв"
    assert history[0].prediction == "positive"


def test_history_isolated_by_user() -> None:
    repo = FakePredictionRepository()
    service = PredictionService(FakeClassifier(), repo)
    service.analyze(user_id=1, text="отзыв первого")
    service.analyze(user_id=2, text="отзыв второго")
    assert len(service.history(user_id=1)) == 1
    assert len(service.history(user_id=2)) == 1


def test_history_empty_for_new_user() -> None:
    service = PredictionService(FakeClassifier(), FakePredictionRepository())
    assert service.history(user_id=999) == []
