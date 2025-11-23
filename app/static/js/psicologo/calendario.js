document.addEventListener('DOMContentLoaded', async function () {
  const calendarEl = document.getElementById('calendar');

  // Cargar citas desde backend
  const citasResponse = await fetch('/api/citas/listar');
  const citas = await citasResponse.json();

  // Convertir citas en eventos sin restricciones
  const eventos = citas.map(c => {
    return {
      title: c.estado
        ? c.estado.charAt(0).toUpperCase() + c.estado.slice(1)
        : 'Cita',
      start: `${c.fecha}T${c.horainicio}`,
      end: `${c.fecha}T${c.horafin}`,
      classNames: [
        c.estado === 'pendiente'  ? 'cita-pendiente'  :
        c.estado === 'aceptada'   ? 'cita-aceptada'   :
        c.estado === 'cancelada'  ? 'cita-cancelada'  :
        'cita-ocupada'
      ],
      editable: false
    };
  });

  // Inicializar calendario
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

    validRange: function(nowDate) {
      return {
        start: new Date(nowDate.getFullYear(), nowDate.getMonth(), nowDate.getDate())
      };
    },

    // Colorear fines de semana y el día actual
    dayCellDidMount: function (info) {
      const hoy = new Date();
      const isToday = info.date.toDateString() === hoy.toDateString();

      if (info.date.getDay() === 0 || info.date.getDay() === 6) {
        info.el.style.backgroundColor = '#D3D3D3';
      }
      if (isToday) {
        info.el.style.backgroundColor = '#A4FDE7';
      }
    },

    // ⛔ Psychologist cannot click
    dateClick: function () {
      Swal.fire(
        'Acceso restringido',
        'No puedes agendar citas desde una cuenta de psicólogo.',
        'warning'
      );
    }
  });

  calendar.render();
});
