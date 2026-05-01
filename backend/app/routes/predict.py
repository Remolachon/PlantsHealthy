"""
predict.py — Router de FastAPI para el endpoint de predicción.

Expone:
  POST /api/predict   — Analiza una imagen y devuelve resultados por hoja.

El endpoint acepta el archivo bajo cualquier nombre de campo en el
multipart/form-data (image, file, photo, etc.) para máxima compatibilidad
con distintos frontends y clientes HTTP.
"""

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse

from app.schemas.response import PredictResponse, ErrorResponse
from app.services.image_processing import decode_image_bytes
from app.services.detection_service import run_detection
from app.utils.helpers import validate_image_content_type
from app.core.logging_config import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/predict", tags=["Predicción"])

# Nombres de campo que se buscan en el form-data, en orden de prioridad.
_ACCEPTED_FIELD_NAMES = ("image", "file", "photo", "img", "imagen")


@router.post(
    "",
    response_model=PredictResponse,
    summary="Detectar y clasificar hojas en una imagen",
    responses={
        400: {"model": ErrorResponse, "description": "Imagen inválida o no encontrada."},
        500: {"model": ErrorResponse, "description": "Error interno del servidor."},
    },
)
async def predict(request: Request) -> PredictResponse:
    """
    Recibe una imagen de planta vía multipart/form-data y ejecuta el pipeline:

    1. Búsqueda flexible del campo de archivo (image, file, photo…).
    2. Validación del tipo de archivo.
    3. Segmentación con Watershed.
    4. División por Convexity Defects.
    5. Clasificación hoja a hoja con TensorFlow.
    6. Corrección heurística por color HSV.
    7. Respuesta con resultados por hoja, resumen e imagen anotada en Base64.
    """
    # 1. Parsear el form-data
    try:
        form = await request.form()
    except Exception as exc:
        logger.warning("No se pudo parsear el formulario: %s", exc)
        raise HTTPException(
            status_code=400,
            detail="La petición debe ser multipart/form-data con un campo de imagen.",
        )

    # Log de diagnóstico: muestra los campos recibidos
    received_fields = list(form.keys())
    logger.info("Campos recibidos en el form-data: %s", received_fields)

    # 2. Buscar el archivo en los nombres conocidos
    upload = None
    matched_field = None
    for field_name in _ACCEPTED_FIELD_NAMES:
        if field_name in form:
            upload = form[field_name]
            matched_field = field_name
            break

    # Si no encontró ninguno conocido, intentar con el primero disponible
    if upload is None and received_fields:
        matched_field = received_fields[0]
        upload = form[matched_field]
        logger.info(
            "Campo '%s' no está en la lista conocida, usando el primero disponible: '%s'",
            _ACCEPTED_FIELD_NAMES, matched_field,
        )

    if upload is None:
        raise HTTPException(
            status_code=400,
            detail=(
                f"No se encontró ningún archivo en el formulario. "
                f"Campos recibidos: {received_fields}. "
                f"Envía la imagen bajo uno de estos nombres: {list(_ACCEPTED_FIELD_NAMES)}."
            ),
        )

    # Verificar que sea un archivo (UploadFile) y no un campo de texto
    if not hasattr(upload, "read"):
        raise HTTPException(
            status_code=400,
            detail=(
                f"El campo '{matched_field}' no contiene un archivo. "
                f"Asegúrate de enviar el Content-Type como multipart/form-data."
            ),
        )

    logger.info("Archivo recibido en campo '%s': '%s'", matched_field, upload.filename)

    # 3. Validar tipo de archivo
    try:
        validate_image_content_type(upload.content_type, upload.filename)
    except ValueError as exc:
        logger.warning("Tipo de archivo rechazado: %s", exc)
        raise HTTPException(status_code=400, detail=str(exc))

    # 4. Leer y decodificar la imagen
    try:
        file_bytes = await upload.read()
        img_bgr = decode_image_bytes(file_bytes)
    except ValueError as exc:
        logger.warning("Error decodificando imagen '%s': %s", upload.filename, exc)
        raise HTTPException(status_code=400, detail=str(exc))

    # 5. Ejecutar pipeline de detección
    logger.info("Procesando imagen '%s'…", upload.filename)
    try:
        result = run_detection(img_bgr)
    except RuntimeError as exc:
        logger.error("Error en el pipeline de detección: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc))
    except Exception as exc:
        logger.exception("Error inesperado procesando '%s'.", upload.filename)
        raise HTTPException(
            status_code=500,
            detail=f"Error inesperado al procesar la imagen: {exc}",
        )

    return result
