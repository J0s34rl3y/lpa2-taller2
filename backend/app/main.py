from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from services.generador import GeneradorFacturas
from models.factura import Factura

app = FastAPI(
    title="API Generador de Facturas",
    description="API para generar facturas sinteticas con datos en español",
    version="1.0.0"
)

# Configurar CORS para permitir peticiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://frontend:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instancia del generador
generador = GeneradorFacturas()


@app.get("/")
def read_root():
    """Endpoint raiz con informacion de la API"""
    return {
        "mensaje": "API Generador de Facturas",
        "version": "1.0.0",
        "endpoints": {
            "generar_factura": "/api/factura/{numero_factura}",
            "documentacion": "/docs"
        }
    }


@app.get("/api/factura/{numero_factura}", response_model=Factura)
def generar_factura(numero_factura: str):
    """
    Genera una factura con datos sinteticos
    
    - **numero_factura**: Numero unico de la factura (ej: FAC-2025-001)
    """
    try:
        factura = generador.generar_factura(numero_factura)
        return factura
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar factura: {str(e)}")


@app.get("/health")
def health_check():
    """Endpoint para verificar el estado del servicio"""
    return {"status": "ok", "servicio": "backend-api"}

    return factura

