"""
config.py — Configuración central de la aplicación.
Todos los parámetros ajustables se definen aquí como constantes tipadas.
"""

import numpy as np
from pathlib import Path

# ---------------------------------------------------------------------------
# Rutas
# ---------------------------------------------------------------------------
BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent   # /backend/
MODEL_PATH: Path = BASE_DIR / "models" / "plant_health_classifier_local.h5"

# ---------------------------------------------------------------------------
# Modelo / inferencia
# ---------------------------------------------------------------------------
IMG_SIZE: int = 128          # Tamaño de entrada del modelo (px)
MAX_WORKERS: int = 4         # Hilos en el ThreadPoolExecutor

# ---------------------------------------------------------------------------
# Filtrado de contornos
# ---------------------------------------------------------------------------
MIN_CONTOUR_AREA: float = 2000.0   # Área mínima para considerar un contorno como hoja
MAX_ASPECT_RATIO: float = 4.0      # Ratio ancho/alto máximo
MIN_SOLIDITY: float = 0.5          # Solidez mínima (área / área del hull)
MIN_SUBCONTOUR_AREA: float = MIN_CONTOUR_AREA * 0.5  # Área mínima de sub-contornos

# ---------------------------------------------------------------------------
# Segmentación HSV (incluye verde + amarillo para hojas marchitas)
# ---------------------------------------------------------------------------
LOWER_HSV: np.ndarray = np.array([15, 40, 40], dtype=np.uint8)
UPPER_HSV: np.ndarray = np.array([100, 255, 255], dtype=np.uint8)

# Rango de Hue para la corrección heurística por color
HUE_GREEN_MIN: int = 35
HUE_GREEN_MAX: int = 85

# ---------------------------------------------------------------------------
# Watershed / morfología
# ---------------------------------------------------------------------------
BILATERAL_D: int = 9
BILATERAL_SIGMA_COLOR: int = 75
BILATERAL_SIGMA_SPACE: int = 75
MORPH_KERNEL_SIZE: tuple[int, int] = (5, 5)
MORPH_ITERATIONS: int = 2
DISTANCE_THRESHOLD_FACTOR: float = 0.4   # fracción del máximo del distance transform
DILATE_ITERATIONS: int = 3

# ---------------------------------------------------------------------------
# Convexity defects
# ---------------------------------------------------------------------------
DEPTH_THRESHOLD_FACTOR: float = 0.02    # fracción del área del contorno

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
LOG_LEVEL: str = "INFO"
LOG_FORMAT: str = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"

# ---------------------------------------------------------------------------
# API
# ---------------------------------------------------------------------------
API_PREFIX: str = "/api"
API_TITLE: str = "Plant Health Detection API"
API_VERSION: str = "1.0.0"
API_DESCRIPTION: str = (
    "Backend de inferencia para detección de plantas sanas/enfermas. "
    "Utiliza segmentación HSV, Watershed, Convexity Defects y TensorFlow."
)
