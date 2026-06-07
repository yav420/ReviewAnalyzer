"""HTTP-клиент к ML API.

Flask не обращается к модели напрямую — только по HTTP к FastAPI.
Этот модуль инкапсулирует все запросы к ML API.
"""

from __future__ import annotations

from dataclasses import dataclass

import requests
from loguru import logger

from src.config import get_settings


@dataclass
class AnalysisResult:
    """Результат анализа, полученный от ML API."""

    label: str
    confidence: float
    probabilities: dict[str, float]


class MLApiError(Exception):
    """Ошибка обращения к ML API."""


class MLApiClient:
    """Клиент ML API (FastAPI)."""

    def __init__(self, base_url: str | None = None, timeout: float = 10.0) -> None:
        self._base_url = base_url or get_settings().ml_api_base_url
        self._timeout = timeout

    def analyze(self, text: str) -> AnalysisResult:
        """Отправляет текст в ML API и возвращает результат анализа."""
        url = f"{self._base_url}/predict"
        try:
            response = requests.post(url, json={"text": text}, timeout=self._timeout)
            response.raise_for_status()
        except requests.RequestException as exc:
            logger.error(f"Ошибка запроса к ML API: {exc}")
            raise MLApiError(str(exc)) from exc

        data = response.json()
        return AnalysisResult(
            label=data["label"],
            confidence=data["confidence"],
            probabilities=data["probabilities"],
        )

    def health(self) -> bool:
        """Проверяет доступность ML API."""
        try:
            response = requests.get(f"{self._base_url}/health", timeout=self._timeout)
            return response.status_code == 200
        except requests.RequestException:
            return False
