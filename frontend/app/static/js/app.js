let facturaActual = null;

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('facturaForm');
    const descargarBtn = document.getElementById('descargarPDF');
    
    form.addEventListener('submit', generarFactura);
    descargarBtn.addEventListener('click', descargarPDF);
});

async function generarFactura(e) {
    e.preventDefault();
    
    const numeroFactura = document.getElementById('numeroFactura').value.trim();
    
    if (!numeroFactura) {
        mostrarAlerta('Por favor ingrese un numero de factura', 'danger');
        return;
    }
    
    try {
        mostrarCargando(true);
        
        const response = await fetch(`/api/obtener-factura/${numeroFactura}`);
        
        if (!response.ok) {
            throw new Error('Error al obtener la factura');
        }
        
        const factura = await response.json();
        facturaActual = numeroFactura;
        
        mostrarFactura(factura);
        mostrarAlerta('Factura generada exitosamente', 'success');
        
    } catch (error) {
        console.error('Error:', error);
        mostrarAlerta('Error al generar la factura. Por favor intente nuevamente.', 'danger');
    } finally {
        mostrarCargando(false);
    }
}

function mostrarFactura(factura) {
    document.getElementById('previewNumero').textContent = factura.numero_factura;
    document.getElementById('previewFecha').textContent = factura.fecha_emision;
    
    document.getElementById('previewEmpresaNombre').textContent = factura.empresa.nombre;
    document.getElementById('previewEmpresaDireccion').textContent = factura.empresa.direccion;
    document.getElementById('previewEmpresaTelefono').textContent = factura.empresa.telefono;
    document.getElementById('previewEmpresaEmail').textContent = factura.empresa.email;
    
    document.getElementById('previewClienteNombre').textContent = factura.cliente.nombre;
    document.getElementById('previewClienteDireccion').textContent = factura.cliente.direccion;
    document.getElementById('previewClienteTelefono').textContent = factura.cliente.telefono;
    
    const detalleBody = document.getElementById('previewDetalle');
    detalleBody.innerHTML = '';
    
    factura.detalle.forEach(item => {
        const subtotal = item.cantidad * item.precio_unitario;
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${item.producto}</td>
            <td><span class="badge bg-secondary">${item.categoria}</span></td>
            <td class="text-center">${item.cantidad}</td>
            <td class="text-end">$${formatearNumero(item.precio_unitario)}</td>
            <td class="text-end">$${formatearNumero(subtotal)}</td>
        `;
        detalleBody.appendChild(row);
    });
    
    document.getElementById('previewSubtotal').textContent = '$' + formatearNumero(factura.subtotal);
    document.getElementById('previewImpuesto').textContent = '$' + formatearNumero(factura.impuesto);
    document.getElementById('previewTotal').textContent = '$' + formatearNumero(factura.total);
    
    document.getElementById('facturaPreview').style.display = 'block';
    
    document.getElementById('facturaPreview').scrollIntoView({ 
        behavior: 'smooth', 
        block: 'start' 
    });
}

async function descargarPDF() {
    if (!facturaActual) {
        mostrarAlerta('No hay factura para descargar', 'warning');
        return;
    }
    
    try {
        mostrarCargando(true);
        
        const response = await fetch(`/api/generar-pdf/${facturaActual}`);
        
        if (!response.ok) {
            throw new Error('Error al generar el PDF');
        }
        
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `factura_${facturaActual}.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        mostrarAlerta('PDF descargado exitosamente', 'success');
        
    } catch (error) {
        console.error('Error:', error);
        mostrarAlerta('Error al descargar el PDF. Por favor intente nuevamente.', 'danger');
    } finally {
        mostrarCargando(false);
    }
}

function mostrarAlerta(mensaje, tipo) {
    const alertContainer = document.getElementById('alertContainer');
    
    const alert = document.createElement('div');
    alert.className = `alert alert-${tipo} alert-dismissible fade show`;
    alert.setAttribute('role', 'alert');
    alert.innerHTML = `
        ${mensaje}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    alertContainer.innerHTML = '';
    alertContainer.appendChild(alert);
    
    setTimeout(() => {
        alert.remove();
    }, 5000);
}

function mostrarCargando(mostrar) {
    const btn = document.querySelector('#facturaForm button[type="submit"]');
    
    if (mostrar) {
        btn.disabled = true;
        btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Generando...';
    } else {
        btn.disabled = false;
        btn.innerHTML = 'Generar Factura';
    }
}

function formatearNumero(numero) {
    return new Intl.NumberFormat('es-CO', {
        minimumFractionDigits: 0,
        maximumFractionDigits: 2
    }).format(numero);
}

