"""
helpers.py — Utilidades generales de la aplicación.
"""

from __future__ import annotations

ALLOWED_CONTENT_TYPES = {
    "image/jpeg",
    "image/png",
    "image/bmp",
    "image/tiff",
    "image/webp",
}

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif", ".webp"}


def validate_image_content_type(content_type: str | None, filename: str | None) -> None:
    """
    Valida que el archivo recibido sea una imagen aceptada.

    Comprueba tanto el Content-Type como la extensión del nombre de archivo.
    Lanza ValueError con un mensaje descriptivo si la validación falla.

    Args:
        content_type: MIME type del archivo (puede ser None).
        filename: Nombre original del archivo (puede ser None).
    """
    # Validar por Content-Type si está disponible
    if content_type and content_type.split(";")[0].strip() in ALLOWED_CONTENT_TYPES:
        return

    # Fallback: validar por extensión
    if filename:
        ext = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
        if ext in ALLOWED_EXTENSIONS:
            return

    raise ValueError(
        f"Tipo de archivo no soportado (content_type='{content_type}', "
        f"filename='{filename}'). "
        f"Formatos aceptados: JPEG, PNG, BMP, TIFF, WEBP."
    )
