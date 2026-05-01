"""
response.py — Esquemas Pydantic para las respuestas de la API.
"""

from typing import Literal
from pydantic import BaseModel, Field


class LeafResult(BaseModel):
    label: Literal["healthy", "diseased"] = Field(
        ..., description="Clasificación de la hoja."
    )
    confidence: float = Field(
        ..., ge=0.0, le=1.0, description="Confianza del modelo (0–1)."
    )
    bbox: list[int] = Field(
        ..., min_length=4, max_length=4,
        description="Bounding box [x, y, w, h] en píxeles."
    )
    color_correction: str = Field(
        default="",
        description="Si se aplicó corrección heurística de color, describe la razón."
    )


class Summary(BaseModel):
    healthy: int = Field(..., ge=0, description="Número de hojas sanas detectadas.")
    diseased: int = Field(..., ge=0, description="Número de hojas enfermas detectadas.")
    total: int = Field(..., ge=0, description="Total de hojas procesadas.")


class PredictResponse(BaseModel):
    leaves: list[LeafResult] = Field(
        ..., description="Resultados por cada hoja detectada."
    )
    summary: Summary = Field(..., description="Resumen global de la imagen.")
    image: str = Field(
        ..., description="Imagen anotada en Base64 (JPEG)."
    )


class ErrorResponse(BaseModel):
    detail: str = Field(..., description="Descripción del error.")
