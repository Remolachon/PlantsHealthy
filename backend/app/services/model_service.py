"""
model_service.py — Carga y gestión del modelo TensorFlow como Singleton.

El modelo se carga una sola vez (lazy loading) al primer acceso
y se reutiliza en todas las peticiones subsiguientes.
"""

import threading
from typing import Optional

import tensorflow as tf

from app.core.config import MODEL_PATH
from app.core.logging_config import get_logger

logger = get_logger(__name__)

_lock = threading.Lock()
_model: Optional[tf.keras.Model] = None


def get_model() -> tf.keras.Model:
    """
    Devuelve la instancia global del modelo.
    Carga desde disco en el primer llamado (thread-safe).

    Raises:
        FileNotFoundError: si el archivo .h5 no existe.
        RuntimeError: si el modelo no pudo cargarse.
    """
    global _model
    if _model is None:
        with _lock:
            if _model is None:   # double-checked locking
                _model = _load_model()
    return _model


def _load_model() -> tf.keras.Model:
    """Carga el modelo desde disco y lo retorna."""
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Modelo no encontrado en '{MODEL_PATH}'. "
            "Asegúrate de colocar 'plant_health_classifier_local.h5' "
            "dentro de la carpeta 'models/'."
        )

    logger.info("Cargando modelo TensorFlow desde '%s'…", MODEL_PATH)
    try:
        model = tf.keras.models.load_model(str(MODEL_PATH))
        logger.info("Modelo cargado exitosamente.")
        return model
    except Exception as exc:
        logger.exception("Error al cargar el modelo.")
        raise RuntimeError(f"No se pudo cargar el modelo: {exc}") from exc
