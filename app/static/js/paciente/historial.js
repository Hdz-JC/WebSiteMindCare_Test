document.addEventListener("DOMContentLoaded", async function() {
  const urlParams = new URLSearchParams(window.location.search);
  const userId = urlParams.get("user_id");

  if (!userId) {
    console.error("No se encontró el ID del usuario en la URL");
    return;
  }

  try {
    const response = await fetch(`/api/historial/${userId}`);
    const data = await response.json();

    const tbody = document.querySelector("#tablaHistorial tbody");
    tbody.innerHTML = "";

    if (data.length === 0) {
      tbody.innerHTML = `
        <tr><td colspan="7">No tienes citas registradas.</td></tr>
      `;
      return;
    }

    data.forEach(cita => {
      const row = document.createElement("tr");

      row.innerHTML = `
        <td>${cita.idcita}</td>
        <td>${cita.fecha}</td>
        <td>${cita.horainicio}</td>
        <td>${cita.horafin}</td>
        <td>${cita.estado}</td>
        <td>${cita.descripcioncancelado || "—"}</td>
        <td>${cita.psicologo_nombre}</td>
      `;

      tbody.appendChild(row);
    });
  } catch (error) {
    console.error("Error al obtener el historial:", error);
  }
});
