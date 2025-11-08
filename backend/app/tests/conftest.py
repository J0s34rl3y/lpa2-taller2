import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Agregar el directorio app al path para imports
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def client():
    """Fixture que proporciona un cliente de prueba para la API"""
    from main import app
    return TestClient(app)


@pytest.fixture
def numero_factura_test():
    """Fixture que proporciona un numero de factura para testing"""
    return "FAC-TEST-001"
