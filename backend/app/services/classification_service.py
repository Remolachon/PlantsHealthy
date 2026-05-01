"""
classification_service.py — Lógica de clasificación de hojas.

Contiene:
  - Corrección heurística de color (HSV).
  - Clasificación individual de hoja con el modelo TensorFlow.
"""

from __future__ import annotations

import numpy as np
import cv2

from app.core.config import HUE_GREEN_MIN, HUE_GREEN_MAX
from app.core.logging_config import get_logger

logger = get_logger(__name__)

# Índices de clase
CLASS_HEALTHY = 0
CLASS_DISEASED = 1
CLASS_LABELS = {CLASS_HEALTHY: "healthy", CLASS_DISEASED: "diseased"}


# ---------------------------------------------------------------------------
# Corrección heurística de color
# ---------------------------------------------------------------------------

def color_correction_if_needed(leaf_rgb: np.ndarray, model_idx: int) -> tuple[int, str]:
    """
    Aplica corrección heurística post-modelo basada en el tono dominante de la hoja.

    Si el modelo predice 'diseased' pero el Hue promedio está en el rango verde,
    se corrige la predicción a 'healthy' para evitar falsos positivos.

    Args:
        leaf_rgb: Recorte RGB de la hoja ya segmentada.
        model_idx: Índice de clase predicho por el modelo (0=healthy, 1=diseased).

    Returns:
        Tupla (índice_final, razón_de_corrección).
        La razón es una cadena vacía si no se realizó corrección.
    """
    hsv = cv2.cvtColor(leaf_rgb, cv2.COLOR_RGB2HSV)
    mean_hue = float(np.mean(hsv[:, :, 0]))   # Canal H en [0, 180]

    if model_idx == CLASS_DISEASED and HUE_GREEN_MIN <= mean_hue <= HUE_GREEN_MAX:
        reason = f"Hue medio {mean_hue:.1f} en rango verde → corregido a healthy"
        logger.debug("color_correction: %s", reason)
        return CLASS_HEALTHY, reason

    return model_idx, ""


# ---------------------------------------------------------------------------
# Clasificación de una hoja
# ---------------------------------------------------------------------------

def classify_leaf(
    model,
    leaf_rgb: np.ndarray,
    input_tensor: np.ndarray,
) -> tuple[str, float, str]:
    """
    Clasifica una hoja preprocesada usando el modelo TensorFlow,
    luego aplica la corrección heurística de color.

    Args:
        model: Modelo TensorFlow cargado.
        leaf_rgb: Imagen RGB de la hoja (para la heurística de color).
        input_tensor: Tensor preprocesado shape (1, IMG_SIZE, IMG_SIZE, 3).

    Returns:
        Tupla (label, confidence, color_correction_reason).

    Raises:
        RuntimeError: si el modelo falla durante la inferencia.
    """
    try:
        preds = model.predict(input_tensor, verbose=0)
    except Exception as exc:
        logger.exception("Error durante la inferencia del modelo.")
        raise RuntimeError(f"Inferencia fallida: {exc}") from exc

    raw_idx = int(np.argmax(preds[0]))
    confidence = float(preds[0][raw_idx])

    final_idx, correction_reason = color_correction_if_needed(leaf_rgb, raw_idx)
    label = CLASS_LABELS[final_idx]

    logger.debug(
        "classify_leaf: raw=%s (%.2f) → final=%s correction='%s'",
        CLASS_LABELS[raw_idx], confidence, label, correction_reason,
    )
    return label, confidence, correction_reason
