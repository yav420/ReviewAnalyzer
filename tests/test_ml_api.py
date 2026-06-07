"""Интеграционные тесты ML API (FastAPI).

Классификатор подменяется фейком через dependency_overrides,
поэтому тесты не зависят от наличия обученной модели на диске.
"""

from __future__ import annotations

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from src.ml_api.dependencies import get_classifier
from src.ml_api.main import app

from tests.fakes import FakeClassifier


@pytest.fixture
def client() -> Iterator[TestClient]:
    app.dependency_overrides[get_classifier] = FakeClassifier
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def test_health_endpoint(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_model_info_endpoint(client: TestClient) -> None:
    response = client.get("/model-info")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "fake-classifier"
    assert data["feature_type"] == "text"
    assert "positive" in data["classes"]


def test_predict_endpoint_returns_label(client: TestClient) -> None:
    response = client.post("/predict", json={"text": "отличный товар"})
    assert response.status_code == 200
    data = response.json()
    assert data["label"] == "positive"
    assert 0.0 <= data["confidence"] <= 1.0
    assert "positive" in data["probabilities"]


def test_predict_rejects_empty_text(client: TestClient) -> None:
    response = client.post("/predict", json={"text": ""})
    assert response.status_code == 422


def test_predict_rejects_missing_field(client: TestClient) -> None:
    response = client.post("/predict", json={})
    assert response.status_code == 422
