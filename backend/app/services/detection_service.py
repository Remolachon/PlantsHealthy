"""
detection_service.py — Orquestador principal del pipeline de detección.

Coordina:
  1. Watershed para detectar contornos de hojas.
  2. División por convexity defects.
  3. Segmentación y preprocesamiento de cada hoja.
  4. Clasificación con el modelo TF + corrección heurística.
  5. Construcción de la respuesta estructurada y anotación visual.
"""

from __future__ import annotations

import base64
from concurrent.futures import ThreadPoolExecutor, Future

import cv2
import numpy as np

from app.core.config import MAX_WORKERS
from app.core.logging_config import get_logger
from app.schemas.response import LeafResult, PredictResponse, Summary
from app.services.image_processing import (
    watershed_segmentation,
    split_contour_by_convexity,
    segment_leaf,
    preprocess_for_model,
)
from app.services.classification_service import classify_leaf
from app.services.model_service import get_model

logger = get_logger(__name__)

# Colores para la anotación (BGR)
_COLOR_HEALTHY = (0, 255, 0)   # verde
_COLOR_DISEASED = (0, 0, 255)  # rojo


# ---------------------------------------------------------------------------
# Anotación visual
# ---------------------------------------------------------------------------

def _annotate_leaf(
    annotated: np.ndarray,
    x: int, y: int, w: int, h: int,
    label: str,
    confidence: float,
    correction: str,
) -> None:
    """Dibuja el bounding box y la etiqueta sobre la imagen anotada (in-place)."""
    color = _COLOR_HEALTHY if label == "healthy" else _COLOR_DISEASED
    text = f"{label}: {confidence:.2f}"
    if correction:
        text += " [corr]"

    cv2.rectangle(annotated, (x, y), (x + w, y + h), color, 2)
    cv2.putText(
        annotated, text, (x, max(y - 10, 10)),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2, cv2.LINE_AA,
    )


# ---------------------------------------------------------------------------
# Pipeline principal (ejecutado en un hilo)
# ---------------------------------------------------------------------------

def _process_image(image_bgr: np.ndarray) -> PredictResponse:
    """
    Ejecuta el pipeline completo sobre una imagen BGR:
      Watershed → split → segmentación → clasificación → anotación.

    Args:
        image_bgr: Imagen completa en formato BGR.

    Returns:
        PredictResponse con todas las hojas, resumen e imagen anotada en Base64.
    """
    model = get_model()
    annotated = image_bgr.copy()
    leaves: list[LeafResult] = []

    # 1. Detectar contornos de hojas
    contours = watershed_segmentation(image_bgr)

    if not contours:
        logger.warning("No se detectaron hojas en la imagen.")
        encoded = _encode_image(annotated)
        return PredictResponse(
            leaves=[],
            summary=Summary(healthy=0, diseased=0, total=0),
            image=encoded,
        )

    # 2. Dividir contornos por convexity defects y ordenar por área (ascendente)
    all_subs: list[tuple[np.ndarray, float]] = []
    for cnt in contours:
        for sc in split_contour_by_convexity(cnt):
            all_subs.append((sc, cv2.contourArea(sc)))

    all_subs.sort(key=lambda t: t[1])   # más pequeños primero

    # 3. Procesar cada sub-contorno
    for sub_cnt, _ in all_subs:
        x, y, w, h = cv2.boundingRect(sub_cnt)
        roi_bgr = image_bgr[y : y + h, x : x + w]

        if roi_bgr.size == 0:
            logger.debug("Sub-contorno vacío, omitido.")
            continue

        # 3a. Segmentar la hoja individual
        leaf_rgb = cv2.cvtColor(roi_bgr, cv2.COLOR_BGR2RGB)
        leaf_segmented = segment_leaf(leaf_rgb)

        # 3b. Preprocesar para el modelo
        input_tensor = preprocess_for_model(leaf_segmented)

        # 3c. Clasificar
        try:
            label, confidence, correction = classify_leaf(model, leaf_segmented, input_tensor)
        except RuntimeError as exc:
            logger.error("Error clasificando hoja en (%d,%d): %s", x, y, exc)
            continue

        # 3d. Registrar resultado
        leaves.append(LeafResult(
            label=label,
            confidence=round(confidence, 4),
            bbox=[x, y, w, h],
            color_correction=correction,
        ))

        # 3e. Anotar imagen
        _annotate_leaf(annotated, x, y, w, h, label, confidence, correction)

    # 4. Resumen
    healthy_count = sum(1 for lf in leaves if lf.label == "healthy")
    diseased_count = len(leaves) - healthy_count

    summary = Summary(
        healthy=healthy_count,
        diseased=diseased_count,
        total=len(leaves),
    )

    logger.info(
        "Pipeline completado: %d hojas procesadas (%d sanas, %d enfermas).",
        len(leaves), healthy_count, diseased_count,
    )

    return PredictResponse(
        leaves=leaves,
        summary=summary,
        image=_encode_image(annotated),
    )


def _encode_image(image_bgr: np.ndarray) -> str:
    """Codifica una imagen BGR a Base64 JPEG."""
    success, buffer = cv2.imencode(".jpg", image_bgr)
    if not success:
        raise RuntimeError("No se pudo codificar la imagen anotada a JPEG.")
    return base64.b64encode(buffer.tobytes()).decode("utf-8")


# ---------------------------------------------------------------------------
# Worker con ThreadPoolExecutor
# ---------------------------------------------------------------------------

_executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)


def run_detection(image_bgr: np.ndarray) -> PredictResponse:
    """
    Lanza el pipeline de detección en un hilo del pool y espera el resultado.

    Args:
        image_bgr: Imagen BGR completa.

    Returns:
        PredictResponse con los resultados.

    Raises:
        Exception: propaga cualquier excepción ocurrida dentro del hilo.
    """
    future: Future = _executor.submit(_process_image, image_bgr)
    return future.result()
