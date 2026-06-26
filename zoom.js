// Función para mostrar la imagen seleccionada en el modal
function mostrarImagenModal(rutaImagen) {
    const modalContenido = document.getElementById('imagenModalContenido');
    modalContenido.src = rutaImagen;
    $('#imagenModal').modal('show');
}