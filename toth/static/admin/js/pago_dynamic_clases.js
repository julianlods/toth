document.addEventListener("DOMContentLoaded", function () {
    const usuarioField = document.querySelector("#id_usuario");
    const claseField = document.querySelector("#id_clase");

    if (usuarioField && claseField) {
        usuarioField.addEventListener("change", function () {
            const usuarioId = usuarioField.value;
            if (usuarioId) {
                fetch(`/get_clases/?usuario=${usuarioId}`)
                    .then((response) => response.json())
                    .then((data) => {
                        claseField.innerHTML = "";
                        data.clases.forEach((clase) => {
                            const option = document.createElement("option");
                            option.value = clase.id;
                            option.textContent = clase.titulo;
                            claseField.appendChild(option);
                        });
                    });
            } else {
                claseField.innerHTML = "";
            }
        });
    }
});
