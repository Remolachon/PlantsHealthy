# 🌿 Plant Health Detection API

Backend de inferencia para detectar hojas **sanas** y **enfermas** en imágenes de plantas.
Construido con **FastAPI** + **TensorFlow** + **OpenCV**.

---

## 🏗️ Arquitectura

```
backend/
├── app/
│   ├── main.py                   # Entrypoint FastAPI (CORS, lifespan, routers)
│   ├── core/
│   │   ├── config.py             # Constantes y parámetros configurables
│   │   └── logging_config.py     # Logger centralizado
│   ├── routes/
│   │   └── predict.py            # Endpoint POST /api/predict
│   ├── services/
│   │   ├── model_service.py      # Singleton del modelo TF (lazy loading)
│   │   ├── image_processing.py   # Segmentación HSV, Watershed, Convexity Defects
│   │   ├── classification_service.py  # Inferencia TF + corrección heurística
│   │   └── detection_service.py  # Orquestador del pipeline + ThreadPool
│   ├── schemas/
│   │   └── response.py           # Modelos Pydantic de respuesta
│   └── utils/
│       └── helpers.py            # Validación de tipos de archivo
├── models/
│   └── plant_health_classifier_local.h5   ← coloca aquí tu modelo
├── requirements.txt
└── README.md
```

### Separación de responsabilidades

| Capa | Responsabilidad |
|---|---|
| `routes/` | Recibir petición HTTP, validar entrada, delegar |
| `services/detection_service.py` | Orquestar el pipeline completo |
| `services/image_processing.py` | **Toda** la lógica OpenCV (HSV, Watershed, Convexity Defects) |
| `services/classification_service.py` | Inferencia TF + heurística de color |
| `services/model_service.py` | Singleton thread-safe del modelo |
| `schemas/` | Tipado estricto con Pydantic |
| `core/config.py` | Única fuente de verdad para parámetros |

---

## ⚙️ Instalación

### 1. Clonar / copiar el proyecto

```bash
cd backend/
```

### 2. Crear entorno virtual (recomendado)

```bash
python -m venv plantshealth
source plantshealth/bin/activate        # Linux / macOS
plantshealth\Scripts\activate           # Windows
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Colocar el modelo

Copia `plant_health_classifier_local.h5` dentro de la carpeta `models/`:

```
backend/
└── models/
    └── plant_health_classifier_local.h5   ✅
```

---

## 🚀 Ejecutar el servidor

```bash
# Desde la carpeta /backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

El servidor estará disponible en:

- **API:** `http://localhost:8000`
- **Documentación interactiva (Swagger):** `http://localhost:8000/docs`
- **Documentación alternativa (ReDoc):** `http://localhost:8000/redoc`
- **Health check:** `http://localhost:8000/health`

---

## 📡 Uso de la API

### `POST /api/predict`

Analiza una imagen y clasifica cada hoja detectada.

**Request** — `multipart/form-data`

| Campo | Tipo | Descripción |
|---|---|---|
| `image` | File | Imagen de la planta (JPEG, PNG, BMP, TIFF, WEBP) |

**Ejemplo con `curl`:**

```bash
curl -X POST http://localhost:8000/api/predict \
  -F "image=@mi_planta.jpg"
```

**Ejemplo con Python (`requests`):**

```python
import requests

with open("mi_planta.jpg", "rb") as f:
    response = requests.post(
        "http://localhost:8000/api/predict",
        files={"image": ("mi_planta.jpg", f, "image/jpeg")},
    )

data = response.json()
print(data["summary"])
```

---

### Respuesta exitosa (`200 OK`)

```json
{
  "leaves": [
    {
      "label": "healthy",
      "confidence": 0.9731,
      "bbox": [120, 45, 200, 180],
      "color_correction": ""
    },
    {
      "label": "diseased",
      "confidence": 0.8812,
      "bbox": [340, 60, 190, 170],
      "color_correction": ""
    }
  ],
  "summary": {
    "healthy": 1,
    "diseased": 1,
    "total": 2
  },
  "image": "<base64 JPEG de la imagen anotada>"
}
```

| Campo | Descripción |
|---|---|
| `leaves[].label` | `"healthy"` o `"diseased"` |
| `leaves[].confidence` | Confianza del modelo (0–1) |
| `leaves[].bbox` | `[x, y, w, h]` en píxeles |
| `leaves[].color_correction` | Describe la corrección heurística aplicada (vacío si no hubo) |
| `summary.healthy` | Cantidad de hojas sanas |
| `summary.diseased` | Cantidad de hojas enfermas |
| `summary.total` | Total de hojas procesadas |
| `image` | Imagen anotada con rectángulos en Base64 (JPEG) |

**Para mostrar la imagen anotada en Python:**

```python
import base64
from PIL import Image
from io import BytesIO

img_bytes = base64.b64decode(data["image"])
img = Image.open(BytesIO(img_bytes))
img.show()
```

### `GET /health`

```json
{
  "status": "ok",
  "model_loaded": true,
  "version": "1.0.0"
}
```

---

## 🧠 Pipeline de detección (lógica preservada)

```
Imagen recibida
    │
    ▼
Filtro bilateral (suavizado)
    │
    ▼
Máscara HSV (verde 15–100 H, incluye amarillo = hojas marchitas)
    │
    ▼
Limpieza morfológica (apertura + cierre)
    │
    ▼
Distance Transform → Watershed
    │
    ▼
Filtrado de contornos (área, aspect ratio, solidez)
    │
    ▼
División por Convexity Defects (separa hojas superpuestas)
    │
    ▼
Por cada hoja:
  ├── Segmentación individual (HSV crop)
  ├── Resize 128×128 + normalización
  ├── Inferencia TensorFlow (.h5)
  └── Corrección heurística de color (Hue promedio)
    │
    ▼
Respuesta JSON + imagen anotada Base64
```

---

## ⚠️ Notas importantes

- El modelo **no se entrena** en este backend — solo inferencia.
- `tensorflow-addons` **no es necesario** en producción (solo en `duvan.py` de entrenamiento).
- En producción, cambia `allow_origins=["*"]` en `main.py` por la URL real de tu app móvil.
- Para CPU-only (sin GPU), reemplaza `tensorflow` por `tensorflow-cpu` en `requirements.txt`.
