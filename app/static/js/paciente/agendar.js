document.addEventListener('DOMContentLoaded', async function () {
  const calendarEl = document.getElementById('calendar');

  // ID del usuario logueado (inyectado desde backend, por ejemplo en un script)
  const userId = parseInt(document.getElementById('user_id').value, 10);

  // Fecha actual
  const hoy = new Date();
  const hoyISO = hoy.toISOString().split('T')[0];

  // Cargar citas desde el backend
  const citasResponse = await fetch('/api/citas/listar');
  const citas = await citasResponse.json();

  function getClaseCita(cita) {
  // Si no es del usuario logeado, mostrar como ocupada (azul)
  if (cita.fkidusuario !== userId) {
    return 'cita-ocupada';
  }

  else if(cita.fkidusuario === userId){
    // Si es del usuario logeado, mostrar según estado
    switch (cita.estado) {
      case 'pendiente':
        return 'cita-pendiente';
      case 'aceptada':
        return 'cita-aceptada';
      case 'cancelada':
        return 'cita-cancelada';
      default:
        return '';
    }
  }
}

document.getElementById('verHistorial').addEventListener('click', () => {
  const userId = document.getElementById('user_id').value;
  window.location.href = `/historial/${userId}`;
});



// Convertir citas en eventos para el calendario
const eventos = citas.map(c => {
  const esDelUsuario = c.fkidusuario === userId;

  return {
    title: esDelUsuario
      ? c.estado.charAt(0).toUpperCase() + c.estado.slice(1)  // Pendiente / Aceptada / Cancelada
      : 'Ocupado', // 👈 Para otros usuarios, siempre muestra “Ocupado”
    start: `${c.fecha}T${c.horainicio}`,
    end: `${c.fecha}T${c.horafin}`,
    classNames: [getClaseCita(c)],
    editable: false
  };
});

  // Inicializar el calendario
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
        start: new Date(nowDate.getFullYear(), nowDate.getMonth(), nowDate.getDate()),
      };
    },
    
    dayCellDidMount: function (info) {
      const day = info.date.getDay();
      const isToday = info.date.toDateString() === hoy.toDateString();

      if (day === 0 || day === 6) {
        info.el.style.backgroundColor = '#bdc3c7'; // inhábil
      }
      if (isToday) {
        info.el.style.backgroundColor = '#A4FDE7'; // color del día actual
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

      // Validaciones
      /*
      const dia = info.date.getDay();
      if (dia === 0 || dia === 6) {
        Swal.fire('Día inhábil', 'No puedes agendar en fines de semana.', 'warning');
        return;
      }
      */

      const fechaClick = new Date(fecha);
      if (fechaClick < new Date(hoyISO)) {
        Swal.fire('Fecha inválida', 'No puedes agendar en días pasados.', 'error');
        return;
      }

      const ahora = new Date();
      if (fecha === hoyISO && info.date < ahora) {
        Swal.fire('Hora inválida', 'No puedes agendar en una hora pasada de hoy.', 'error');
        return;
      }

      // Obtener psicólogo real
      const psicologoResponse = await fetch('/api/psicologo');
      const psicologo = await psicologoResponse.json();

      // Confirmar cita
      const result = await Swal.fire({
        title: '¿Agendar cita?',
        html: `
          <p><b>Fecha:</b> ${fecha}</p>
          <p><b>Hora:</b> ${horaInicio} - ${horaFin}</p>
          <p><b>Psicólogo:</b> ${psicologo.nombre} ${psicologo.apellidopaterno}</p>
        `,
        icon: 'question',
        showCancelButton: true,
        confirmButtonText: 'Sí, agendar',
        cancelButtonText: 'Cancelar'
      });

      if (result.isConfirmed) {
        const data = {
          fecha,
          horainicio: horaInicio,
          horafin: horaFin
        };

        // Si la cita es hoy, marcar como aceptada
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
            classNames: [data.estado === 'aceptada' ? 'cita-aceptada' : 'cita-pendiente'],
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