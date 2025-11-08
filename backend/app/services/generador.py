from faker import Faker
from datetime import date
import random
from models.factura import Empresa, Cliente, DetalleProducto, Factura


class GeneradorFacturas:
    """Clase para generar facturas con datos sinteticos en español"""
    
    def __init__(self):
        self.fake = Faker('es_ES')
        
        # Productos colombianos variados por categoria
        self.productos = {
            "Dulces": [
                "Chocolatina Jet", "Bon Bon Bum", "Chocoramo", "Galletas Ducales",
                "Chocolatina Jumbo", "Choclitos", "Nucita", "Gomitas Trululu",
                "Colombina", "Wafer Cream", "Masmelos"
            ],
            "Carnes": [
                "Lomo de res", "Pechuga de pollo", "Carne molida", "Costillas de cerdo",
                "Chuleta ahumada", "Chorizo", "Punta de anca", "Sobrebarriga",
                "Lomo de cerdo", "Pollo entero"
            ],
            "Frutas": [
                "Banano", "Manzana", "Papaya", "Mango", "Guayaba",
                "Lulo", "Maracuya", "Mora", "Fresa", "Naranja",
                "Mandarina", "Piña", "Sandia"
            ],
            "Bebidas": [
                "Gaseosa Colombiana", "Postobon Manzana", "Agua Cristal", "Jugos Hit",
                "Pony Malta", "Cafe Juan Valdez", "Te Hatsu", "Cerveza Aguila",
                "Colombiana", "Coca-Cola", "Jugo de naranja natural"
            ],
            "Lacteos": [
                "Leche Alpina", "Yogurt Alpina", "Queso campesino", "Kumis",
                "Arequipe Alpina", "Mantequilla", "Queso mozzarella", "Crema de leche"
            ],
            "Granos": [
                "Arroz Diana", "Frijol cargamanto", "Lentejas", "Garbanzos",
                "Arveja verde", "Maiz pira", "Quinua"
            ],
            "Aseo": [
                "Jabon Fab", "Detergente Ace", "Suavitel", "Desinfectante",
                "Papel higienico", "Jabon de tocador", "Limpiador Mr Musculo"
            ],
            "Panaderia": [
                "Pan tajado Bimbo", "Pandebono", "Pan Frances", "Mogolla",
                "Pan integral", "Croissant", "Pan de queso"
            ]
        }
        
        # Empresas colombianas tipicas
        self.empresas = [
            "Distribuidora La Esperanza S.A.S",
            "Comercializadora El Trigal Ltda",
            "Supermercados La Canasta S.A",
            "Distribuciones El Ahorro",
            "Almacenes La Rebaja S.A.S",
            "Mayorista San Andresito",
            "Distribuidora El Exito Ltda"
        ]
        
        # Ciudades colombianas
        self.ciudades = [
            "Bogota", "Medellin", "Cali", "Barranquilla", "Cartagena",
            "Bucaramanga", "Pereira", "Manizales", "Ibague", "Cucuta"
        ]
    
    def generar_empresa(self) -> Empresa:
        """Genera datos de una empresa colombiana"""
        ciudad = random.choice(self.ciudades)
        return Empresa(
            nombre=random.choice(self.empresas),
            direccion=f"{self.fake.street_name()} #{random.randint(10, 99)}-{random.randint(10, 99)}, {ciudad}",
            telefono=f"+57 {random.randint(300, 321)} {random.randint(100, 999)} {random.randint(1000, 9999)}",
            email=self.fake.email()
        )
    
    def generar_cliente(self) -> Cliente:
        """Genera datos de un cliente colombiano"""
        ciudad = random.choice(self.ciudades)
        tipo_negocio = random.choice([
            "Supermercado", "Tienda", "Minimercado", "Drogueria",
            "Restaurante", "Cafeteria", "Panaderia"
        ])
        nombre_negocio = f"{tipo_negocio} {self.fake.last_name()}"
        
        return Cliente(
            nombre=nombre_negocio,
            direccion=f"{self.fake.street_name()} #{random.randint(10, 99)}-{random.randint(10, 99)}, {ciudad}",
            telefono=f"+57 {random.randint(300, 321)} {random.randint(100, 999)} {random.randint(1000, 9999)}"
        )
    
    def generar_productos(self, cantidad: int = None) -> list[DetalleProducto]:
        """Genera una lista de productos aleatorios"""
        if cantidad is None:
            cantidad = random.randint(3, 8)
        
        productos = []
        categorias_usadas = random.sample(list(self.productos.keys()), min(cantidad, len(self.productos)))
        
        for categoria in categorias_usadas:
            producto_nombre = random.choice(self.productos[categoria])
            
            # Precios realistas segun categoria
            precios = {
                "Dulces": (800, 3000),
                "Carnes": (15000, 35000),
                "Frutas": (2000, 8000),
                "Bebidas": (1500, 5000),
                "Lacteos": (3000, 12000),
                "Granos": (2000, 8000),
                "Aseo": (5000, 15000),
                "Panaderia": (1000, 4000)
            }
            
            precio_min, precio_max = precios.get(categoria, (1000, 10000))
            
            productos.append(DetalleProducto(
                producto=producto_nombre,
                categoria=categoria,
                cantidad=random.randint(1, 20),
                precio_unitario=random.randint(precio_min, precio_max)
            ))
        
        return productos
    
    def generar_factura(self, numero_factura: str) -> Factura:
        """Genera una factura completa con datos aleatorios"""
        empresa = self.generar_empresa()
        cliente = self.generar_cliente()
        productos = self.generar_productos()
        
        # Calcular totales
        subtotal = sum(p.subtotal for p in productos)
        impuesto = round(subtotal * 0.19, 2)  # IVA del 19%
        total = subtotal + impuesto
        
        return Factura(
            numero_factura=numero_factura,
            fecha_emision=date.today(),
            empresa=empresa,
            cliente=cliente,
            detalle=productos,
            subtotal=subtotal,
            impuesto=impuesto,
            total=total
        )
