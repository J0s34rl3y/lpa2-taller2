from flask import Flask, render_template, request, jsonify, send_file
import requests
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from io import BytesIO
import os

app = Flask(__name__)

# URL del backend
BACKEND_URL = os.getenv('BACKEND_URL', 'http://backend:8000')


@app.route("/")
def index():
    """Pagina principal"""
    return render_template("index.html")


@app.route("/api/obtener-factura/<numero_factura>")
def obtener_factura(numero_factura):
    """Consulta el backend para obtener una factura"""
    try:
        response = requests.get(f"{BACKEND_URL}/api/factura/{numero_factura}")
        response.raise_for_status()
        return jsonify(response.json())
    except requests.RequestException as e:
        return jsonify({"error": f"Error al conectar con el backend: {str(e)}"}), 500


@app.route("/api/generar-pdf/<numero_factura>")
def generar_pdf(numero_factura):
    """Genera un PDF de la factura"""
    try:
        # Obtener datos de la factura desde el backend
        response = requests.get(f"{BACKEND_URL}/api/factura/{numero_factura}")
        response.raise_for_status()
        factura = response.json()
        
        # Crear el PDF en memoria
        buffer = BytesIO()
        pdf = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=50, leftMargin=50,
                               topMargin=50, bottomMargin=50)
        
        # Contenedor de elementos del PDF
        elementos = []
        estilos = getSampleStyleSheet()
        
        # Estilo personalizado para el titulo
        estilo_titulo = ParagraphStyle(
            'CustomTitle',
            parent=estilos['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#D2691E'),
            spaceAfter=30,
            alignment=1  # Centrado
        )
        
        # Estilo para subtitulos
        estilo_subtitulo = ParagraphStyle(
            'CustomSubtitle',
            parent=estilos['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#8B4513'),
            spaceAfter=12
        )
        
        # Titulo
        elementos.append(Paragraph("FACTURA DE VENTA", estilo_titulo))
        elementos.append(Spacer(1, 0.3*inch))
        
        # Informacion de la factura
        info_factura = [
            ['Numero de Factura:', factura['numero_factura']],
            ['Fecha de Emision:', factura['fecha_emision']]
        ]
        tabla_info = Table(info_factura, colWidths=[2*inch, 4*inch])
        tabla_info.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F5DEB3')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#D2691E'))
        ]))
        elementos.append(tabla_info)
        elementos.append(Spacer(1, 0.3*inch))
        
        # Datos de la empresa
        elementos.append(Paragraph("Datos de la Empresa", estilo_subtitulo))
        empresa = factura['empresa']
        datos_empresa = [
            ['Nombre:', empresa['nombre']],
            ['Direccion:', empresa['direccion']],
            ['Telefono:', empresa['telefono']],
            ['Email:', empresa['email']]
        ]
        tabla_empresa = Table(datos_empresa, colWidths=[1.5*inch, 4.5*inch])
        tabla_empresa.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#FFE4B5')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
        ]))
        elementos.append(tabla_empresa)
        elementos.append(Spacer(1, 0.2*inch))
        
        # Datos del cliente
        elementos.append(Paragraph("Datos del Cliente", estilo_subtitulo))
        cliente = factura['cliente']
        datos_cliente = [
            ['Nombre:', cliente['nombre']],
            ['Direccion:', cliente['direccion']],
            ['Telefono:', cliente['telefono']]
        ]
        tabla_cliente = Table(datos_cliente, colWidths=[1.5*inch, 4.5*inch])
        tabla_cliente.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#FFE4B5')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
        ]))
        elementos.append(tabla_cliente)
        elementos.append(Spacer(1, 0.3*inch))
        
        # Detalle de productos
        elementos.append(Paragraph("Detalle de Productos", estilo_subtitulo))
        datos_productos = [['Producto', 'Categoria', 'Cantidad', 'P. Unitario', 'Subtotal']]
        for item in factura['detalle']:
            subtotal_item = item['cantidad'] * item['precio_unitario']
            datos_productos.append([
                item['producto'],
                item['categoria'],
                str(item['cantidad']),
                f"${item['precio_unitario']:,.0f}",
                f"${subtotal_item:,.0f}"
            ])
        
        tabla_productos = Table(datos_productos, colWidths=[2*inch, 1.3*inch, 0.8*inch, 1*inch, 1*inch])
        tabla_productos.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#D2691E')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#8B4513')),
            ('FONTSIZE', (0, 1), (-1, -1), 9)
        ]))
        elementos.append(tabla_productos)
        elementos.append(Spacer(1, 0.3*inch))
        
        # Totales
        datos_totales = [
            ['Subtotal:', f"${factura['subtotal']:,.2f}"],
            ['Impuesto (IVA 19%):', f"${factura['impuesto']:,.2f}"],
            ['TOTAL:', f"${factura['total']:,.2f}"]
        ]
        tabla_totales = Table(datos_totales, colWidths=[4*inch, 2*inch])
        tabla_totales.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (0, 2), (1, 2), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('FONTSIZE', (0, 2), (1, 2), 14),
            ('TEXTCOLOR', (0, 2), (1, 2), colors.HexColor('#D2691E')),
            ('BACKGROUND', (1, 2), (1, 2), colors.HexColor('#FFE4B5')),
            ('LINEABOVE', (0, 2), (-1, 2), 2, colors.HexColor('#D2691E')),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8)
        ]))
        elementos.append(tabla_totales)
        
        # Construir el PDF
        pdf.build(elementos)
        buffer.seek(0)
        
        return send_file(
            buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'factura_{numero_factura}.pdf'
        )
        
    except requests.RequestException as e:
        return jsonify({"error": f"Error al conectar con el backend: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Error al generar PDF: {str(e)}"}), 500


@app.route("/health")
def health_check():
    """Endpoint para verificar el estado del servicio"""
    return jsonify({"status": "ok", "servicio": "frontend-web"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)

