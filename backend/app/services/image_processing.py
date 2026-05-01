"""
image_processing.py — Lógica de procesamiento de imágenes con OpenCV.

Contiene:
  - Decodificación de bytes a imagen BGR.
  - Segmentación de hoja individual (HSV, igual que en entrenamiento).
  - Preprocesamiento para el modelo (resize + normalización).
  - Filtrado de contornos por área, aspect ratio y solidez.
  - Watershed para separar hojas superpuestas.
  - División de contornos mediante Convexity Defects.
"""

from __future__ import annotations

import numpy as np
import cv2

from app.core.config import (
    IMG_SIZE,
    LOWER_HSV,
    UPPER_HSV,
    MIN_CONTOUR_AREA,
    MAX_ASPECT_RATIO,
    MIN_SOLIDITY,
    MIN_SUBCONTOUR_AREA,
    BILATERAL_D,
    BILATERAL_SIGMA_COLOR,
    BILATERAL_SIGMA_SPACE,
    MORPH_KERNEL_SIZE,
    MORPH_ITERATIONS,
    DISTANCE_THRESHOLD_FACTOR,
    DILATE_ITERATIONS,
    DEPTH_THRESHOLD_FACTOR,
)
from app.core.logging_config import get_logger

logger = get_logger(__name__)


# ---------------------------------------------------------------------------
# Decodificación
# ---------------------------------------------------------------------------

def decode_image_bytes(file_bytes: bytes) -> np.ndarray:
    """
    Decodifica bytes crudos a una imagen en formato BGR (NumPy array).

    Args:
        file_bytes: Contenido binario del archivo de imagen.

    Returns:
        Imagen BGR como ndarray.

    Raises:
        ValueError: si los bytes están vacíos o no corresponden a una imagen válida.
    """
    if not file_bytes:
        raise ValueError("El archivo recibido está vacío.")

    np_arr = np.frombuffer(file_bytes, dtype=np.uint8)
    img_bgr = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    if img_bgr is None:
        raise ValueError(
            "No se pudo decodificar la imagen. "
            "Asegúrate de enviar un formato válido (JPEG, PNG, BMP, etc.)."
        )
    return img_bgr


# ---------------------------------------------------------------------------
# Segmentación individual de hoja (idéntica a la usada en entrenamiento)
# ---------------------------------------------------------------------------

def segment_leaf(image_rgb: np.ndarray) -> np.ndarray:
    """
    Segmenta una hoja individual usando umbralización en el espacio HSV.
    El rango HSV incluye verde (sano) y amarillo (marchito) para consistencia
    con el conjunto de datos de entrenamiento.

    Args:
        image_rgb: Imagen en RGB (NumPy array).

    Returns:
        Recorte de la hoja en RGB. Si no se detecta contorno, devuelve la imagen completa.
    """
    img_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, LOWER_HSV, UPPER_HSV)

    kernel = np.ones(MORPH_KERNEL_SIZE, np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        largest = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest)
        leaf_bgr = img_bgr[y : y + h, x : x + w]
    else:
        logger.debug("segment_leaf: no se encontraron contornos, se usa imagen completa.")
        leaf_bgr = img_bgr

    return cv2.cvtColor(leaf_bgr, cv2.COLOR_BGR2RGB)


# ---------------------------------------------------------------------------
# Preprocesamiento para el modelo
# ---------------------------------------------------------------------------

def preprocess_for_model(leaf_rgb: np.ndarray) -> np.ndarray:
    """
    Redimensiona y normaliza una hoja RGB para la inferencia del modelo.

    Args:
        leaf_rgb: Imagen RGB de la hoja (tamaño arbitrario).

    Returns:
        Tensor shape (1, IMG_SIZE, IMG_SIZE, 3) con valores en [0, 1].
    """
    leaf_resized = cv2.resize(leaf_rgb, (IMG_SIZE, IMG_SIZE))
    leaf_norm = leaf_resized.astype(np.float32) / 255.0
    return np.expand_dims(leaf_norm, axis=0)


# ---------------------------------------------------------------------------
# Filtrado de contornos
# ---------------------------------------------------------------------------

def is_valid_contour(cnt: np.ndarray) -> bool:
    """
    Evalúa si un contorno representa una hoja plausible según:
      - Área mínima.
      - Aspect ratio dentro de rango permitido.
      - Solidez mínima (área / área del hull convexo).

    Args:
        cnt: Contorno de OpenCV.

    Returns:
        True si el contorno pasa todos los filtros.
    """
    area = cv2.contourArea(cnt)
    if area < MIN_CONTOUR_AREA:
        return False

    x, y, w, h = cv2.boundingRect(cnt)
    if w == 0 or h == 0:
        return False

    aspect_ratio = float(w) / float(h)
    if aspect_ratio > MAX_ASPECT_RATIO or aspect_ratio < 1.0 / MAX_ASPECT_RATIO:
        return False

    hull = cv2.convexHull(cnt)
    hull_area = cv2.contourArea(hull)
    if hull_area == 0:
        return False

    solidity = float(area) / float(hull_area)
    if solidity < MIN_SOLIDITY:
        return False

    return True


# ---------------------------------------------------------------------------
# Watershed
# ---------------------------------------------------------------------------

def watershed_segmentation(image_bgr: np.ndarray) -> list[np.ndarray]:
    """
    Aplica el algoritmo Watershed para separar hojas superpuestas en la imagen.

    Pipeline:
      1. Filtro bilateral para suavizar preservando bordes.
      2. Máscara HSV (verde + amarillo).
      3. Limpieza morfológica (apertura + cierre).
      4. Distance Transform → marcadores de regiones seguras.
      5. Watershed sobre los marcadores.
      6. Extracción y filtrado de contornos resultantes.

    Args:
        image_bgr: Imagen completa en BGR.

    Returns:
        Lista de contornos válidos (uno por hoja detectada).
    """
    # 1. Suavizar con filtro bilateral
    blurred = cv2.bilateralFilter(
        image_bgr, d=BILATERAL_D,
        sigmaColor=BILATERAL_SIGMA_COLOR,
        sigmaSpace=BILATERAL_SIGMA_SPACE,
    )

    # 2. Máscara HSV
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, LOWER_HSV, UPPER_HSV)

    # 3. Limpieza morfológica
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, MORPH_KERNEL_SIZE)
    mask_open = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=MORPH_ITERATIONS)
    mask_close = cv2.morphologyEx(mask_open, cv2.MORPH_CLOSE, kernel, iterations=MORPH_ITERATIONS)

    # 4. Distance Transform → foreground seguro
    dist = cv2.distanceTransform(mask_close, cv2.DIST_L2, 5)
    _, sure_fg = cv2.threshold(dist, DISTANCE_THRESHOLD_FACTOR * dist.max(), 255, 0)
    sure_fg = np.uint8(sure_fg)

    # 5. Background seguro y región desconocida
    sure_bg = cv2.dilate(mask_close, kernel, iterations=DILATE_ITERATIONS)
    unknown = cv2.subtract(sure_bg, sure_fg)

    # 6. Marcadores para Watershed
    _, markers = cv2.connectedComponents(sure_fg)
    markers = markers + 1
    markers[unknown == 255] = 0

    img_ws = blurred.copy()
    markers = cv2.watershed(img_ws, markers)

    # 7. Máscara final y contornos
    final_mask = np.zeros_like(mask_close)
    final_mask[markers > 1] = 255
    contours, _ = cv2.findContours(final_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    valid = [c for c in contours if is_valid_contour(c)]
    logger.debug("watershed_segmentation: %d contornos válidos encontrados.", len(valid))
    return valid


# ---------------------------------------------------------------------------
# División por Convexity Defects
# ---------------------------------------------------------------------------

def split_contour_by_convexity(cnt: np.ndarray) -> list[np.ndarray]:
    """
    Divide un contorno en sub-contornos separando por puntos de convexity defects
    pronunciados. Útil cuando varias hojas están físicamente tocándose.

    Args:
        cnt: Contorno de OpenCV.

    Returns:
        Lista de sub-contornos. Si no hay defectos relevantes, devuelve [cnt].
    """
    cnt_pts = cnt.reshape(-1, 2)
    hull_indices = cv2.convexHull(cnt, returnPoints=False)

    if hull_indices is None or len(hull_indices) < 3:
        return [cnt]

    defects = cv2.convexityDefects(cnt, hull_indices)
    if defects is None:
        return [cnt]

    depth_threshold = DEPTH_THRESHOLD_FACTOR * cv2.contourArea(cnt)
    split_indices: list[int] = []

    for i in range(defects.shape[0]):
        _, _, f_idx, depth = defects[i, 0]
        if depth > depth_threshold:
            split_indices.append(int(f_idx))

    if not split_indices:
        return [cnt]

    split_indices = sorted(set(split_indices))
    pts = cnt_pts.tolist()
    n = len(pts)
    sub_contours: list[np.ndarray] = []
    prev_idx = 0

    for idx in split_indices:
        part = pts[prev_idx : idx + 1]
        if len(part) > 2:
            sc = np.array(part, dtype=np.int32).reshape(-1, 1, 2)
            if cv2.contourArea(sc) >= MIN_SUBCONTOUR_AREA:
                sub_contours.append(sc)
        prev_idx = idx + 1

    # Segmento final (cierra el ciclo)
    if prev_idx < n:
        part = pts[prev_idx:] + pts[: split_indices[0] + 1]
        if len(part) > 2:
            sc = np.array(part, dtype=np.int32).reshape(-1, 1, 2)
            if cv2.contourArea(sc) >= MIN_SUBCONTOUR_AREA:
                sub_contours.append(sc)

    return sub_contours if sub_contours else [cnt]
