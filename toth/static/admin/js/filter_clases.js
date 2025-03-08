document.addEventListener("DOMContentLoaded", function () {
    const usuarioField = document.querySelector("#id_usuario");
    const claseField = document.querySelector("#id_clase");

    if (usuarioField) {
        usuarioField.addEventListener("change", function () {
            const usuarioId = this.value;
            if (!usuarioId) {
                claseField.innerHTML = "<option value=''>---------</option>";
                return;
            }

            fetch(`/api/get-clases/?usuario_id=${usuarioId}`)
                .then((response) => response.json())
                .then((data) => {
                    claseField.innerHTML = "<option value=''>---------</option>";
                    data.forEach((clase) => {
                        const option = document.createElement("option");
                        option.value = clase.id;
                        option.textContent = clase.titulo;
                        claseField.appendChild(option);
                    });
                })
                .catch((error) => console.error("Error al cargar las clases:", error));
        });
    }
});
