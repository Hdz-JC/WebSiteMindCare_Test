document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("form-nota");

    if (!form) return; // Evitar errores si el form no existe

    form.addEventListener("submit", async function (e) {
        e.preventDefault();

        const boton = form.querySelector("button");
        const citaId = boton.getAttribute("data-cita-id");

        const tituloInput = form.querySelector("input[name='titulo']");
        const contenidoInput = form.querySelector("textarea[name='contenido']");

        if (!tituloInput || !contenidoInput) {
            alert("No se encontraron los campos de título o contenido.");
            return;
        }

        const titulo = tituloInput.value.trim();
        const contenido = contenidoInput.value.trim();

        if (!titulo || !contenido) {
            alert("Debe completar título y contenido.");
            return;
        }

        try {
            const response = await fetch("/api/notas/agregar", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    idcita: citaId,
                    titulo: titulo,
                    contenido: contenido
                })
            });

            if (response.ok) {
                alert("Nota guardada correctamente.");
                tituloInput.value = "";
                contenidoInput.value = "";
            } else {
                const errorData = await response.json();
                alert("Error al guardar la nota: " + (errorData.error || "desconocido"));
            }
        } catch (err) {
            console.error(err);
            alert("Error en la conexión con el servidor.");
        }
    });
});
