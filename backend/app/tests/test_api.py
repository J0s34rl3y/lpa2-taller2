import pytest
from fastapi.testclient import TestClient


class TestAPIEndpoints:
    """Tests para los endpoints de la API"""
    
    def test_read_root(self, client):
        """Test del endpoint raiz"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "mensaje" in data
        assert data["mensaje"] == "API Generador de Facturas"
        assert "version" in data
        assert "endpoints" in data
    
    def test_health_check(self, client):
        """Test del endpoint de health check"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["servicio"] == "backend-api"
    
    def test_generar_factura_exitoso(self, client, numero_factura_test):
        """Test de generacion exitosa de factura"""
        response = client.get(f"/api/factura/{numero_factura_test}")
        assert response.status_code == 200
        
        data = response.json()
        
        # Verificar estructura basica
        assert "numero_factura" in data
        assert data["numero_factura"] == numero_factura_test
        assert "fecha_emision" in data
        assert "empresa" in data
        assert "cliente" in data
        assert "detalle" in data
        assert "subtotal" in data
        assert "impuesto" in data
        assert "total" in data
    
    def test_estructura_empresa(self, client, numero_factura_test):
        """Test de la estructura de datos de empresa"""
        response = client.get(f"/api/factura/{numero_factura_test}")
        data = response.json()
        empresa = data["empresa"]
        
        assert "nombre" in empresa
        assert "direccion" in empresa
        assert "telefono" in empresa
        assert "email" in empresa
        assert isinstance(empresa["nombre"], str)
        assert len(empresa["nombre"]) > 0
    
    def test_estructura_cliente(self, client, numero_factura_test):
        """Test de la estructura de datos del cliente"""
        response = client.get(f"/api/factura/{numero_factura_test}")
        data = response.json()
        cliente = data["cliente"]
        
        assert "nombre" in cliente
        assert "direccion" in cliente
        assert "telefono" in cliente
        assert isinstance(cliente["nombre"], str)
        assert len(cliente["nombre"]) > 0
    
    def test_estructura_detalle_productos(self, client, numero_factura_test):
        """Test de la estructura de detalle de productos"""
        response = client.get(f"/api/factura/{numero_factura_test}")
        data = response.json()
        detalle = data["detalle"]
        
        assert isinstance(detalle, list)
        assert len(detalle) > 0
        
        # Verificar primer producto
        primer_producto = detalle[0]
        assert "producto" in primer_producto
        assert "categoria" in primer_producto
        assert "cantidad" in primer_producto
        assert "precio_unitario" in primer_producto
        
        assert isinstance(primer_producto["cantidad"], int)
        assert primer_producto["cantidad"] > 0
        assert isinstance(primer_producto["precio_unitario"], (int, float))
        assert primer_producto["precio_unitario"] > 0
    
    def test_calculos_factura(self, client, numero_factura_test):
        """Test de los calculos de la factura"""
        response = client.get(f"/api/factura/{numero_factura_test}")
        data = response.json()
        
        # Calcular subtotal manualmente
        subtotal_calculado = sum(
            item["cantidad"] * item["precio_unitario"] 
            for item in data["detalle"]
        )
        
        assert data["subtotal"] == subtotal_calculado
        
        # Verificar impuesto (19%)
        impuesto_esperado = round(subtotal_calculado * 0.19, 2)
        assert abs(data["impuesto"] - impuesto_esperado) < 0.01
        
        # Verificar total
        total_esperado = subtotal_calculado + data["impuesto"]
        assert abs(data["total"] - total_esperado) < 0.01
    
    def test_multiples_facturas_diferentes(self, client):
        """Test que verifica que cada factura generada es diferente"""
        response1 = client.get("/api/factura/FAC-001")
        response2 = client.get("/api/factura/FAC-002")
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        data1 = response1.json()
        data2 = response2.json()
        
        # Las facturas deben tener numeros diferentes
        assert data1["numero_factura"] != data2["numero_factura"]


class TestModelos:
    """Tests para validacion de modelos"""
    
    def test_tipos_de_datos(self, client, numero_factura_test):
        """Test de tipos de datos en la respuesta"""
        response = client.get(f"/api/factura/{numero_factura_test}")
        data = response.json()
        
        assert isinstance(data["numero_factura"], str)
        assert isinstance(data["fecha_emision"], str)
        assert isinstance(data["subtotal"], (int, float))
        assert isinstance(data["impuesto"], (int, float))
        assert isinstance(data["total"], (int, float))
        assert isinstance(data["empresa"], dict)
        assert isinstance(data["cliente"], dict)
        assert isinstance(data["detalle"], list)
    
    def test_valores_positivos(self, client, numero_factura_test):
        """Test que verifica que los valores monetarios sean positivos"""
        response = client.get(f"/api/factura/{numero_factura_test}")
        data = response.json()
        
        assert data["subtotal"] >= 0
        assert data["impuesto"] >= 0
        assert data["total"] >= 0
        
        for item in data["detalle"]:
            assert item["cantidad"] > 0
            assert item["precio_unitario"] > 0
    
    def test_categorias_validas(self, client, numero_factura_test):
        """Test que verifica que las categorias de productos sean validas"""
        response = client.get(f"/api/factura/{numero_factura_test}")
        data = response.json()
        
        categorias_validas = [
            "Dulces", "Carnes", "Frutas", "Bebidas", 
            "Lacteos", "Granos", "Aseo", "Panaderia"
        ]
        
        for item in data["detalle"]:
            assert item["categoria"] in categorias_validas


class TestGeneradorFacturas:
    """Tests para el servicio GeneradorFacturas"""
    
    def test_generador_crea_productos(self):
        """Test que el generador crea productos correctamente"""
        from services.generador import GeneradorFacturas
        
        generador = GeneradorFacturas()
        productos = generador.generar_productos(cantidad=5)
        
        assert len(productos) == 5
        for producto in productos:
            assert hasattr(producto, 'producto')
            assert hasattr(producto, 'categoria')
            assert hasattr(producto, 'cantidad')
            assert hasattr(producto, 'precio_unitario')
    
    def test_generador_crea_empresa(self):
        """Test que el generador crea empresas correctamente"""
        from services.generador import GeneradorFacturas
        
        generador = GeneradorFacturas()
        empresa = generador.generar_empresa()
        
        assert hasattr(empresa, 'nombre')
        assert hasattr(empresa, 'direccion')
        assert hasattr(empresa, 'telefono')
        assert hasattr(empresa, 'email')
        assert len(empresa.nombre) > 0
    
    def test_generador_crea_cliente(self):
        """Test que el generador crea clientes correctamente"""
        from services.generador import GeneradorFacturas
        
        generador = GeneradorFacturas()
        cliente = generador.generar_cliente()
        
        assert hasattr(cliente, 'nombre')
        assert hasattr(cliente, 'direccion')
        assert hasattr(cliente, 'telefono')
        assert len(cliente.nombre) > 0
    
    def test_generador_factura_completa(self):
        """Test que el generador crea facturas completas"""
        from services.generador import GeneradorFacturas
        
        generador = GeneradorFacturas()
        factura = generador.generar_factura("TEST-001")
        
        assert factura.numero_factura == "TEST-001"
        assert factura.subtotal > 0
        assert factura.impuesto > 0
        assert factura.total > 0
        assert len(factura.detalle) > 0
