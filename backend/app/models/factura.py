from pydantic import BaseModel, Field
from typing import List
from datetime import date


class Empresa(BaseModel):
    """Modelo que representa los datos de la empresa emisora"""
    nombre: str = Field(..., description="Nombre de la empresa")
    direccion: str = Field(..., description="Direccion de la empresa")
    telefono: str = Field(..., description="Telefono de contacto")
    email: str = Field(..., description="Correo electronico")


class Cliente(BaseModel):
    """Modelo que representa los datos del cliente"""
    nombre: str = Field(..., description="Nombre del cliente")
    direccion: str = Field(..., description="Direccion del cliente")
    telefono: str = Field(..., description="Telefono del cliente")


class DetalleProducto(BaseModel):
    """Modelo que representa cada producto de la factura"""
    producto: str = Field(..., description="Nombre del producto")
    categoria: str = Field(..., description="Categoria del producto")
    cantidad: int = Field(..., gt=0, description="Cantidad de productos")
    precio_unitario: float = Field(..., gt=0, description="Precio unitario del producto")
    
    @property
    def subtotal(self) -> float:
        """Calcula el subtotal del producto"""
        return self.cantidad * self.precio_unitario


class Factura(BaseModel):
    """Modelo completo de la factura"""
    numero_factura: str = Field(..., description="Numero unico de factura")
    fecha_emision: date = Field(..., description="Fecha de emision de la factura")
    empresa: Empresa = Field(..., description="Datos de la empresa emisora")
    cliente: Cliente = Field(..., description="Datos del cliente")
    detalle: List[DetalleProducto] = Field(..., min_length=1, description="Lista de productos")
    subtotal: float = Field(..., ge=0, description="Subtotal de la factura")
    impuesto: float = Field(..., ge=0, description="Impuesto aplicado (IVA)")
    total: float = Field(..., ge=0, description="Total a pagar")
    
    class Config:
        json_schema_extra = {
            "example": {
                "numero_factura": "FAC-2025-001",
                "fecha_emision": "2025-08-15",
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
                    }
                ],
                "subtotal": 14400,
                "impuesto": 2736,
                "total": 17136
            }
        }
