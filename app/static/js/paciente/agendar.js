document.addEventListener('DOMContentLoaded', async function () {
    const calendarEl = document.getElementById('calendar');


    const TIME_ZONE = 'America/Tijuana'; 

    const userId = parseInt(document.getElementById('user_id').value, 10);

    // Fecha actual: Usamos la hora de Tijuana para una validación consistente.

    const hoyTZString = new Date().toLocaleString('en-US', { timeZone: TIME_ZONE });
    const hoy = new Date(hoyTZString); 

    const year = hoy.getFullYear();
    const month = String(hoy.getMonth() + 1).padStart(2, '0');
    const day = String(hoy.getDate()).padStart(2, '0');
    const hoyISO = `${year}-${month}-${day}`;
    
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
    const eventos = citas
        .filter(c => c.estado !== 'cancelada') 
        .map(c => {
            const esDelUsuario = c.fkidusuario === userId;

            // DETECTAR SI ES UN DÍA BLOQUEADO
            const esBloqueoDia = (c.horainicio === '00:00:00' || c.horainicio === '00:00');

            if (esBloqueoDia) {
                return {
                    title: 'NO LABORAL',
                    start: c.fecha,      
                    display: 'background', 
                    backgroundColor: '#ff9f89', 
                    classNames: ['dia-bloqueado'],
                    editable: false,
                    allDay: true
                };
            }

            // CITA NORMAL

            return {
                title: esDelUsuario
                    ? c.estado.charAt(0).toUpperCase() + c.estado.slice(1) 
                    : 'Ocupado',  
                start: `${c.fecha}T${c.horainicio}`,
                end: `${c.fecha}T${c.horafin}`,
                classNames: [getClaseCita(c)],
                editable: false
            };
        });

    // Inicializar el calendario
    const calendar = new FullCalendar.Calendar(calendarEl, {
        contentHeight: 'auto',
        initialView: 'timeGridWeek',
        locale: 'es',
        dayHeaderFormat: { weekday: 'long', day: 'numeric' },
        allDaySlot: false,
        slotMinTime: '05:00:00',
        slotMaxTime: '24:00:00', // 🟢 CAMBIO: Extendido hasta las 12 AM (medianoche del día siguiente)
        slotDuration: '01:00:00',
        slotLabelFormat: { hour: 'numeric', hour12: true },
        headerToolbar: {
            left: 'prev',
            center: 'title',
            right: 'today next'
        },
        buttonText: { today: 'Hoy' },
        events: eventos,

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
            // 1. RECUPERAR DEFINICIONES BÁSICAS
            const fecha = info.dateStr.split('T')[0];
            const horaInicio = info.date.toLocaleTimeString('en-GB', {
                hour: '2-digit', minute: '2-digit', second: '2-digit'
            });
            // Calcular hora fin (1 hora después)
            const horaFinObj = new Date(info.date.getTime() + 60 * 60 * 1000);
            const horaFin = horaFinObj.toLocaleTimeString('en-GB', {
                hour: '2-digit', minute: '2-digit', second: '2-digit'
            });

            // 2. VALIDACIÓN DE DÍA BLOQUEADO (Por el psicólogo)
            const diaBloqueado = citas.some(c => 
                c.fecha === fecha && 
                c.estado !== 'cancelada' && 
                (c.horainicio === '00:00:00' || c.horainicio === '00:00')
            );

            if (diaBloqueado) {
                Swal.fire({
                    icon: 'warning',
                    title: 'Día Inhábil',
                    text: 'El psicólogo ha marcado este día como no laborable.'
                });
                return; // Detiene la función
            }

            // 3. OTRAS VALIDACIONES (Fines de semana y pasado)
            const dia = info.date.getDay();
            if (dia === 0 || dia === 6) {
                Swal.fire('Día inhábil', 'No puedes agendar en fines de semana.', 'warning');
                return;
            }

            // Usamos 'hoy' (hora de Tijuana) para la comparación
            const ahora = hoy; 
            
            // A) Validar días pasados (Ayer, antier...)
            if (fecha < hoyISO) {
                Swal.fire('Fecha inválida', 'No puedes agendar citas en días pasados.', 'error');
                return;
            }

            // B) Validar hora pasada en el día de hoy
            // Se agrega un margen de 1 minuto (60000ms) por latencia.
            if (fecha === hoyISO && info.date.getTime() <= (ahora.getTime() + 60000)) { 
                Swal.fire('Hora inválida', 'Esa hora ya pasó. Por favor selecciona un horario futuro.', 'error');
                return;
            }

            // 4. OBTENER PSICÓLOGO Y CONFIRMAR
            try {
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
                        fecha: fecha,
                        horainicio: horaInicio,
                        horafin: horaFin,
                        estado: 'pendiente' 
                    };
                    
                    const resp = await fetch('/api/citas', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(data)
                    });

                    const json = await resp.json();

                    if (resp.ok) {
                        Swal.fire('Éxito', 'Cita agendada correctamente', 'success');
                        calendar.addEvent({
                            title: 'Pendiente', 
                            start: `${fecha}T${horaInicio}`,
                            end: `${fecha}T${horaFin}`,
                            classNames: ['cita-pendiente'], 
                            editable: false
                        });
                    } else {
                        Swal.fire('Error', json.error || 'No se pudo agendar la cita', 'error');
                    }
                }
            } catch (error) {
                console.error(error);
                Swal.fire('Error', 'Ocurrió un error al procesar la solicitud', 'error');
            }
        }
    });

    calendar.render();
});