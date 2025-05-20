document.addEventListener("DOMContentLoaded", function () {
    const usuarioField = document.querySelector("#id_usuario");
    const claseField = document.querySelector("#id_clase");

    if (!usuarioField || !claseField) return;

    usuarioField.addEventListener("change", function () {
        const usuarioId = this.value;

        if (!usuarioId) {
            claseField.innerHTML = "";
            return;
        }

        fetch(`/get_clases/?usuario_id=${usuarioId}`)
            .then((response) => response.json())
            .then((data) => {
                claseField.innerHTML = "";

                if (data.length === 0) {
                    const option = document.createElement("option");
                    option.textContent = "No hay clases para este usuario";
                    option.disabled = true;
                    option.selected = true;
                    claseField.appendChild(option);
                    return;
                }

                data.forEach((clase) => {
                    const option = document.createElement("option");
                    option.value = clase.id;
                    option.textContent = clase.titulo;
                    claseField.appendChild(option);
                });
            })
            .catch((error) => {
                console.error("Error al cargar clases:", error);
            });
    });
});
