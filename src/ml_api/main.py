"""Точка входа ML API (FastAPI).

Запуск в контейнере:
    uvicorn src.ml_api.main:app --host 0.0.0.0 --port 8000
"""

from __future__ import annotations

import sys

from fastapi import FastAPI
from loguru import logger

from src.ml_api.routers import prediction, system

logger.remove()
logger.add(sys.stdout, level="INFO")
logger.add(sys.stderr, level="ERROR")


def create_app() -> FastAPI:
    """Собирает и настраивает приложение FastAPI."""
    app = FastAPI(
        title="ReviewAnalyzer ML API",
        description="Сервис анализа тональности отзывов",
        version="1.0.0",
    )
    app.include_router(system.router)
    app.include_router(prediction.router)
    logger.info("ML API инициализирован")
    return app


app = create_app()
