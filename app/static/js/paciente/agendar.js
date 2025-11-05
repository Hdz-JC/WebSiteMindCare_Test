document.addEventListener('DOMContentLoaded', async function () {
  const calendarEl = document.getElementById('calendar');

  // Obtenemos la fecha actual
  const hoy = new Date();
  const hoyISO = hoy.toISOString().split('T')[0];

  // Cargar citas desde el backend
  const citasResponse = await fetch('/api/citas/listar');
  const citas = await citasResponse.json();

  // Convertir citas en eventos para el calendario
  const eventos = citas.map(c => ({
    title: c.estado === 'aceptada' ? 'Ocupado' : 'Pendiente',
    start: `${c.fecha}T${c.horainicio}`,
    end: `${c.fecha}T${c.horafin}`,
    backgroundColor:
      c.estado === 'aceptada' ? '#e74c3c' : '#f1c40f',
    borderColor:
      c.estado === 'aceptada' ? '#e74c3c' : '#f1c40f',
    editable: false
  }));

  const calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'timeGridWeek',
    locale: 'es',
    dayHeaderFormat: { weekday: 'long', day: 'numeric' },
    allDaySlot: false,
    slotMinTime: '10:00:00',
    slotMaxTime: '21:00:00',
    slotDuration: '01:00:00',
    slotLabelFormat: { hour: 'numeric', hour12: true },
    headerToolbar: {
      left: 'prev',
      center: 'title',
      right: 'today next'
    },
    buttonText: { today: 'Hoy' },
    events: eventos,

    // Deshabilitar días pasados
    validRange: { start: hoyISO },

    // Colorear sábados y domingos como inhábiles
    dayCellDidMount: function (info) {
      const day = info.date.getDay();
      const isToday = info.date.toDateString() === hoy.toDateString();

      if (day === 0 || day === 6) {
        info.el.style.backgroundColor = '#bdc3c7'; // gris (inhábil)
      }
      if (isToday) {
        info.el.style.backgroundColor = '#3498db'; // azul (día de hoy)
      }
    },

    dateClick: async function (info) {
      const fecha = info.dateStr.split('T')[0];
      const horaInicio = info.date.toLocaleTimeString('en-GB', {
        hour: '2-digit', minute: '2-digit', second: '2-digit'
      });

      const horaFinObj = new Date(info.date.getTime() + 60 * 60 * 1000);
      const horaFin = horaFinObj.toLocaleTimeString('en-GB', {
        hour: '2-digit', minute: '2-digit', second: '2-digit'
      });

      // No permitir sábados ni domingos
      const dia = info.date.getDay();
      if (dia === 0 || dia === 6) {
        Swal.fire('Día inhábil', 'No puedes agendar en fines de semana.', 'warning');
        return;
      }

      // No permitir días pasados
      if (info.date < hoy) {
        Swal.fire('Fecha inválida', 'No puedes agendar en días pasados.', 'error');
        return;
      }

      // Mostrar confirmación
      const result = await Swal.fire({
        title: '¿Agendar cita?',
        html: `
          <p><b>Fecha:</b> ${fecha}</p>
          <p><b>Hora:</b> ${horaInicio} - ${horaFin}</p>
          <p><b>Psicólogo:</b> Predeterminado</p>
        `,
        icon: 'question',
        showCancelButton: true,
        confirmButtonText: 'Sí, agendar',
        cancelButtonText: 'Cancelar'
      });

      if (result.isConfirmed) {
        const data = {
          fecha: fecha,
          horainicio: horaInicio,
          horafin: horaFin
        };

        // Si la cita es hoy, marcamos como aceptada
        if (fecha === hoyISO) data.estado = 'aceptada';

        const resp = await fetch('/api/citas', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data)
        });

        const json = await resp.json();

        if (resp.ok) {
          Swal.fire('Éxito', 'Cita agendada correctamente', 'success');
          calendar.addEvent({
            title: data.estado === 'aceptada' ? 'Ocupado' : 'Pendiente',
            start: `${fecha}T${horaInicio}`,
            end: `${fecha}T${horaFin}`,
            backgroundColor: data.estado === 'aceptada' ? '#e74c3c' : '#f1c40f',
            borderColor: data.estado === 'aceptada' ? '#e74c3c' : '#f1c40f',
            editable: false
          });
        } else {
          Swal.fire('Error', json.error || 'No se pudo agendar la cita', 'error');
        }
      }
    }
  });

  calendar.render();
});
