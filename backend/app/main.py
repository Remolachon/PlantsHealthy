"""
main.py — Punto de entrada de la aplicación FastAPI.

Configura:
  - Logging.
  - Aplicación FastAPI con metadatos.
  - CORS (permisivo en desarrollo; restringir en producción).
  - Routers.
  - Eventos de inicio (precarga del modelo).
  - Health-check endpoint.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import API_TITLE, API_VERSION, API_DESCRIPTION, API_PREFIX
from app.core.logging_config import setup_logging, get_logger
from app.routes.predict import router as predict_router
from app.services.model_service import get_model

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
setup_logging()
logger = get_logger(__name__)


# ---------------------------------------------------------------------------
# Lifespan (startup / shutdown)
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Precarga el modelo en startup para que la primera petición no sea lenta."""
    logger.info("🚀 Iniciando aplicación — precargando modelo TensorFlow…")
    try:
        get_model()
        logger.info("✅ Modelo listo.")
    except Exception as exc:
        logger.critical("❌ No se pudo cargar el modelo: %s", exc)
        raise

    yield  # La aplicación corre aquí

    logger.info("👋 Cerrando aplicación.")


# ---------------------------------------------------------------------------
# Instancia FastAPI
# ---------------------------------------------------------------------------

app = FastAPI(
    title=API_TITLE,
    version=API_VERSION,
    description=API_DESCRIPTION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)


# ---------------------------------------------------------------------------
# CORS — permitir cualquier origen en desarrollo.
# En producción reemplaza allow_origins=["*"] con la URL de tu app móvil.
# ---------------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Rutas
# ---------------------------------------------------------------------------

app.include_router(predict_router, prefix=API_PREFIX)


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------

@app.get("/health", tags=["Sistema"], summary="Verificar estado del servidor")
async def health_check() -> dict:
    """Devuelve el estado del servidor y si el modelo está cargado."""
    try:
        get_model()
        model_ok = True
    except Exception:
        model_ok = False

    return {
        "status": "ok" if model_ok else "degraded",
        "model_loaded": model_ok,
        "version": API_VERSION,
    }
