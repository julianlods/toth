document.addEventListener('DOMContentLoaded', function () {
    const usuarioField = document.querySelector('#id_usuario');
    const claseField = document.querySelector('#id_clase');

    if (usuarioField && claseField) {
        usuarioField.addEventListener('change', function () {
            const usuarioId = this.value;

            // Realiza una solicitud AJAX para actualizar las clases
            fetch(`/api/get-clases/${usuarioId}/`)
                .then(response => response.json())
                .then(data => {
                    // Limpia las opciones actuales
                    claseField.innerHTML = '';

                    // Agrega las nuevas opciones
                    data.forEach(clase => {
                        const option = document.createElement('option');
                        option.value = clase.id;
                        option.textContent = clase.titulo;
                        claseField.appendChild(option);
                    });
                });
        });
    }
});
