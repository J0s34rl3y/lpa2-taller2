# Generador de Facturas

Sistema completo de generacion de facturas utilizando FastAPI para el backend que genera datos sinteticos con Faker, y Flask para el frontend que permite generar PDFs profesionales con ReportLab.

## Autor

Jose Arley - @J0s34rl3y

## Descripcion General

Es un sistema completo de generacion de facturas con datos sinteticos en español, que representa productos variados de Colombia (dulces, carnes, frutas, bebidas, lacteos, granos, aseo y panaderia). El sistema consta de dos servicios principales:

- **Backend API (FastAPI)**: Genera datos sinteticos de facturas en español con productos colombianos
- **Frontend Web (Flask)**: Interfaz web moderna con diseño calido que consume el API y genera PDFs descargables

## Arquitectura

```
┌────────────────┐          ┌───────────────┐
│  Frontend Web  │ ───────> │  Backend API  │
│  puerto 3000   │   HTTP   │  puerto 8000  │
│  Flask + RLab  │ <─────── │  FastAPI      │
└────────────────┘          └───────────────┘
```

## Estructura del Proyecto

```
lpa2-taller2/
├── docker-compose.yml
├── README.md
├── .pre-commit-config.yaml
├── pyproject.toml
├── .gitignore
├── backend/
│   ├── Dockerfile
│   └── app/
│       ├── main.py
│       ├── requirements.txt
│       ├── pytest.ini
│       ├── .coveragerc
│       ├── models/
│       │   ├── __init__.py
│       │   └── factura.py
│       ├── services/
│       │   ├── __init__.py
│       │   └── generador.py
│       └── tests/
│           ├── __init__.py
│           ├── conftest.py
│           └── test_api.py
└── frontend/
    ├── Dockerfile
    └── app/
        ├── main.py
        ├── requirements.txt
        ├── static/
        │   ├── css/
        │   │    └── style.css
        │   └── js/
        │        └── app.js
        └── templates/
            └── index.html
```

## Requerimientos Tecnicos

### Backend
- FastAPI 0.115.0
- Uvicorn 0.32.0
- Faker 30.8.2
- Pydantic 2.9.2
- Pytest 8.3.3
- Pytest-cov 5.0.0
- HTTPx 0.27.2
- Ruff 0.7.2
- Black 24.10.0

### Frontend
- Flask 3.0.3
- ReportLab 4.2.5
- Requests 2.32.3
- Bootstrap 5.3.0 (CDN)

### Contenedores
- Docker
- Docker Compose

## Inicio Rapido

### Prerrequisitos

- Docker instalado
- Docker Compose instalado
- Git

### Instalacion y Ejecucion

1. **Clonar el repositorio**

```bash
git clone https://github.com/J0s34rl3y/lpa2-taller2.git
cd lpa2-taller2
```

2. **Construir y levantar los servicios**

```bash
docker-compose up --build
```

3. **Acceder a la aplicacion**

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Documentacion Swagger**: http://localhost:8000/docs

## Uso del Sistema

### Interfaz Web (Frontend)

1. Abrir el navegador en `http://localhost:3000`
2. Ingresar un numero de factura (ejemplo: `FAC-2025-001`)
3. Hacer clic en "Generar Factura"
4. Ver la vista previa de la factura generada
5. Hacer clic en "Descargar PDF" para obtener el archivo

### API Backend

El backend expone los siguientes endpoints:

#### Endpoint Principal

**GET** `/api/factura/{numero_factura}`

Genera una factura con datos sinteticos en español.

**Ejemplo de uso:**

```bash
curl http://localhost:8000/api/factura/FAC-2025-001
```

**Ejemplo de Respuesta:**

```json
{
  "numero_factura": "FAC-2025-001",
  "fecha_emision": "2025-11-08",
  "empresa": {
    "nombre": "Distribuidora La Esperanza S.A.S",
    "direccion": "Calle 12 #45-67, Cali",
    "telefono": "+57 311 567 8901",
    "email": "contacto@laesperanza.com"
  },
  "cliente": {
    "nombre": "Supermercado Los Andes",
    "direccion": "Carrera 50 #23-90, Medellin",
    "telefono": "+57 312 908 4567"
  },
  "detalle": [
    {
      "producto": "Chocolatina Jet",
      "categoria": "Dulces",
      "cantidad": 12,
      "precio_unitario": 1200
    },
    {
      "producto": "Lomo de res",
      "categoria": "Carnes",
      "cantidad": 5,
      "precio_unitario": 24000
    },
    {
      "producto": "Gaseosa Colombiana",
      "categoria": "Bebidas",
      "cantidad": 10,
      "precio_unitario": 2800
    }
  ],
  "subtotal": 147000,
  "impuesto": 27930,
  "total": 174930
}
```

#### Otros Endpoints

- **GET** `/` - Informacion de la API
- **GET** `/health` - Estado del servicio
- **GET** `/docs` - Documentacion interactiva Swagger

## Caracteristicas Especiales

### Datos en Español

Todos los datos generados estan en español y utilizan:
- Nombres de empresas colombianas tipicas
- Direcciones con formato colombiano
- Numeros de telefono con codigo +57
- Productos colombianos autenticos por categoria:
  - Dulces: Chocolatina Jet, Bon Bon Bum, Chocoramo, etc.
  - Carnes: Lomo de res, Pechuga de pollo, etc.
  - Frutas: Banano, Mango, Lulo, Maracuya, etc.
  - Bebidas: Gaseosa Colombiana, Postobon, Pony Malta, etc.
  - Lacteos: Leche Alpina, Yogurt Alpina, Kumis, etc.
  - Y mas categorias...

### Diseño Moderno

El frontend utiliza:
- **Bootstrap 5** para diseño responsive
- **Paleta de colores calida**: tonos naranjas, beige, marron
- **Interfaz minimalista** y profesional
- **Animaciones suaves** y transiciones
- **Vista previa interactiva** de facturas

### PDF Profesional

Los PDFs generados incluyen:
- Encabezado con titulo y logo visual
- Informacion de empresa y cliente en formato de tablas
- Detalle de productos con calculos automaticos
- Totales con IVA del 19%
- Diseño profesional con colores corporativos

## Configuración Avanzada

### Variables de Entorno

Puedes modificar el `docker-compose.yml` para añadir variables de entorno:

```yaml
environment:
  - API_URL=http://backend:8000
  - DEBUG=true
```

## Testing con Pytest

El proyecto incluye una suite completa de tests con pytest y cobertura de codigo.

### Ejecutar Tests

**Dentro del contenedor:**

```bash
# Entrar al contenedor del backend
docker exec -it factura-api bash

# Ejecutar todos los tests
cd /app && pytest tests/ -v

# Ejecutar tests con cobertura
cd /app && pytest tests/ --cov=. --cov-report=term-missing

# Ejecutar tests con reporte HTML
cd /app && pytest tests/ --cov=. --cov-report=html

# Ver reporte de cobertura
# El reporte se genera en htmlcov/index.html
```

**Localmente (sin Docker):**

```bash
# Instalar dependencias
cd backend/app
pip install -r requirements.txt

# Ejecutar tests
pytest tests/ -v

# Con cobertura
pytest tests/ --cov=. --cov-report=term-missing
```

### Tests Incluidos

El proyecto incluye tests para:

- **Endpoints de la API**: Verifican que todos los endpoints funcionan correctamente
- **Modelos de datos**: Validan la estructura de Empresa, Cliente, Factura, etc.
- **Generador de facturas**: Prueban la generacion de datos sinteticos
- **Calculos**: Verifican que subtotales, impuestos y totales sean correctos
- **Validaciones**: Comprueban que los datos cumplan las reglas de negocio

### Cobertura de Codigo

Los tests cubren:
- Endpoints de la API (100%)
- Modelos Pydantic
- Servicio generador de facturas
- Validaciones y calculos

## Pre-commit Hooks

El proyecto esta configurado con pre-commit hooks para mantener la calidad del codigo.

### Instalacion de Pre-commit

```bash
# Instalar pre-commit
pip install pre-commit

# Instalar los hooks
pre-commit install
```

### Hooks Configurados

- **ruff**: Linter para Python (corrige automaticamente)
- **black**: Formateador de codigo Python
- **pytest**: Ejecuta tests antes de cada commit

### Uso

```bash
# Los hooks se ejecutan automaticamente al hacer commit
git commit -m "mensaje"

# Ejecutar hooks manualmente
pre-commit run --all-files

# Actualizar hooks
pre-commit autoupdate
```

## Configuracion de Calidad de Codigo

### Ruff

Configurado en `pyproject.toml` con:
- Longitud de linea: 100 caracteres
- Reglas de pycodestyle, pyflakes, isort
- Verificacion de bugs con flake8-bugbear

### Black

Formateador automatico de codigo:
- Longitud de linea: 100 caracteres
- Compatible con ruff

### Pytest

Configurado en `pytest.ini` con:
- Ejecucion de tests en `tests/`
- Reporte de cobertura automatico
- Markers personalizados para tests lentos e integracion

## Comandos Utiles

### Docker

```bash
# Levantar servicios
docker-compose up

# Levantar en segundo plano
docker-compose up -d

# Reconstruir imagenes
docker-compose up --build

# Ver logs
docker-compose logs -f

# Ver logs de un servicio especifico
docker-compose logs -f backend
docker-compose logs -f frontend

# Detener servicios
docker-compose down

# Detener y eliminar volumenes
docker-compose down -v

# Reiniciar un servicio especifico
docker-compose restart backend
```

### Testing API

```bash
# Endpoint de salud
curl http://localhost:8000/health

# Generar factura
curl http://localhost:8000/api/factura/FAC-2025-001

# Ver documentacion
open http://localhost:8000/docs
```

## Documentacion de la API

La documentacion interactiva esta disponible en:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Desde la documentacion puedes:
- Ver todos los endpoints disponibles
- Probar la API directamente
- Ver esquemas de request/response
- Descargar la especificacion OpenAPI

## Estructura de Archivos Clave

### Backend

- **`main.py`**: Aplicacion FastAPI con endpoints y configuracion CORS
- **`models/factura.py`**: Modelos Pydantic para validacion de datos
- **`services/generador.py`**: Logica de generacion de datos sinteticos con Faker
- **`tests/test_api.py`**: Suite completa de tests
- **`tests/conftest.py`**: Fixtures de pytest
- **`requirements.txt`**: Dependencias del backend

### Frontend

- **`main.py`**: Aplicacion Flask con rutas y generacion de PDF
- **`templates/index.html`**: Interfaz HTML con Bootstrap
- **`static/css/style.css`**: Estilos personalizados con paleta calida
- **`static/js/app.js`**: Logica JavaScript para interaccion
- **`requirements.txt`**: Dependencias del frontend

### Configuracion

- **`docker-compose.yml`**: Orquestacion de servicios
- **`.pre-commit-config.yaml`**: Hooks de pre-commit
- **`pyproject.toml`**: Configuracion de ruff y black
- **`pytest.ini`**: Configuracion de pytest
- **`.coveragerc`**: Configuracion de cobertura

## Tecnologias Utilizadas

### Backend
- **FastAPI**: Framework web moderno y rapido
- **Pydantic**: Validacion de datos con type hints
- **Faker**: Generacion de datos sinteticos
- **Uvicorn**: Servidor ASGI de alto rendimiento
- **Pytest**: Framework de testing

### Frontend
- **Flask**: Micro-framework web de Python
- **ReportLab**: Generacion de PDFs
- **Bootstrap 5**: Framework CSS responsive
- **JavaScript ES6**: Logica del cliente

### DevOps
- **Docker**: Contenedorizacion
- **Docker Compose**: Orquestacion multi-contenedor
- **Pre-commit**: Hooks de calidad de codigo
- **Ruff**: Linter rapido de Python
- **Black**: Formateador de codigo

## Troubleshooting

### El backend no arranca

```bash
# Verificar logs
docker-compose logs backend

# Reconstruir el contenedor
docker-compose up --build backend
```

### El frontend no puede conectar al backend

Verificar que:
1. El backend este corriendo: `curl http://localhost:8000/health`
2. La variable `BACKEND_URL` en `frontend/app/main.py` apunte a `http://backend:8000`
3. Los servicios esten en la misma red de Docker

### Los tests fallan

```bash
# Verificar que las dependencias esten instaladas
docker exec -it factura-api pip list

# Reinstalar dependencias
docker exec -it factura-api pip install -r requirements.txt

# Ejecutar tests con verbose
docker exec -it factura-api bash -c "cd /app && pytest tests/ -vv"
```

### Error al generar PDF

Verificar que ReportLab este instalado correctamente:

```bash
docker exec -it factura-frontend pip show reportlab
```

## Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/NuevaCaracteristica`)
3. Commit tus cambios (`git commit -m 'Agregar nueva caracteristica'`)
4. Push a la rama (`git push origin feature/NuevaCaracteristica`)
5. Abre un Pull Request

## Licencia

Este proyecto es parte del curso de Lenguajes de Programacion Avanzados 2 y esta destinado para fines educativos.

## Contacto

Jose Arley - [@J0s34rl3y](https://github.com/J0s34rl3y)

Link del Proyecto: [https://github.com/J0s34rl3y/lpa2-taller2](https://github.com/J0s34rl3y/lpa2-taller2)

---

Desarrollado con FastAPI, Flask, Docker y mucho cafe

