"""
logging_config.py — Configuración centralizada del logger.
"""

import logging
import sys
from app.core.config import LOG_LEVEL, LOG_FORMAT


def setup_logging() -> None:
    """Configura el logger raíz de la aplicación."""
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL, logging.INFO),
        format=LOG_FORMAT,
        handlers=[logging.StreamHandler(sys.stdout)],
    )


def get_logger(name: str) -> logging.Logger:
    """Devuelve un logger nombrado listo para usar."""
    return logging.getLogger(name)
