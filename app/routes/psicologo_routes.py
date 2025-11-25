from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify, flash
from app.services.impl.psicologo_service_impl import PsicologoServiceImpl
from app.utils.decorator import login_required, role_required
from app.utils.mail_utils import send_email
from datetime import date, datetime, timezone,time
from app.models import Cita, User,Expediente,db
from sqlalchemy import or_



psicologo_bp = Blueprint('psicologo_bp', __name__)
psicologo_service = PsicologoServiceImpl()

@psicologo_bp.route('/api/psicologo', methods=['GET'])
def obtener_psicologo():
    """Devuelve el psicólogo"""
    data = psicologo_service.obtener_psicologo()
    status = 200 if "error" not in data else 404
    return jsonify(data), status

@psicologo_bp.route('/inicio')
@login_required
@role_required('psicologo')
def inicio_psicologo():
    
    # Obtener las citas del día actual (aceptadas)
    user_id = session.get('user_id')
    hoy = date.today()
    try:
        citas = Cita.query.filter(
            Cita.fkidpsicologo == user_id,
            Cita.fecha == hoy,
            Cita.estado.in_(['aceptada', 'pendiente'])
        ).order_by(Cita.horainicio).all()

        # Mostrar los datos en listado (tabla)
        citas_hoy = []
        for c in citas:
            paciente = User.query.get(c.fkidusuario)
            paciente_nombre = f"{paciente.nombre} {paciente.paterno or ''} {paciente.materno or ''}".strip()

            citas_hoy.append({
                'id': c.idcita,
                'fecha': c.fecha,
                'horainicio': c.horainicio.strftime('%H:%M') if c.horainicio else None,
                'horafin': c.horafin.strftime('%H:%M') if c.horafin else None,
                'estado': c.estado,
                'paciente': paciente_nombre
            })

    except Exception as e:
        # Si no hay citas, pasa una lista vacía
        citas_hoy = []

    return render_template('psicologo/inicio_psicologo.html', rol='psicologo', citas_hoy=citas_hoy)

@psicologo_bp.route('/expedientes')
@login_required
def expedientes():
    if session.get('user_rol') != 'psicologo':
        return redirect(url_for('user_bp.inicio'))

    email = request.args.get('email', None)

    query = db.session.query(Expediente).join(User)

    if email:
        query = query.filter(User.email == email)
    else:
        # Si no hay email, ordenamos por id y traemos al primero
        query = query.order_by(User.id)

    expedientes = query.all()

    return render_template('psicologo/expedientes_paciente.html', rol='psicologo', expedientes=expedientes)



@psicologo_bp.route('/notas', methods=['GET', 'POST'])
@login_required
def notas_paciente():
    if session.get('user_rol') != 'psicologo':
        return redirect(url_for('user_bp.inicio'))

    idcita = request.args.get('idcita')
    cita = Cita.query.get(idcita) if idcita else None

    if not cita:
        flash("Cita no encontrada", "error")
        return redirect(url_for('psicologo_bp.inicio_psicologo'))

    paciente = User.query.get(cita.fkidusuario)

    return render_template('psicologo/notas_paciente.html', rol='psicologo', cita=cita, paciente=paciente
    )

@psicologo_bp.route('/api/bloquear-dia', methods=['POST'])
@login_required
@role_required('psicologo')
def bloquear_dia():
    data = request.get_json()
    fecha_str = data.get('fecha')
    user_id = session.get('user_id')

    if not fecha_str:
        return jsonify({'error': 'La fecha es obligatoria'}), 400

    fecha_bloqueo = datetime.strptime(fecha_str, '%Y-%m-%d').date()

    try:
        # 1. CANCELAR CITAS EXISTENTES
        citas_pacientes = Cita.query.filter(
            Cita.fkidpsicologo == user_id,
            Cita.fecha == fecha_bloqueo,
            Cita.fkidusuario != user_id, 
            Cita.estado.in_(['aceptada', 'pendiente'])
        ).all()

        count_canceladas = 0
        
        # --- BUCLE DE CANCELACIÓN Y ENVÍO DE CORREO ---
        for cita in citas_pacientes:
            cita.estado = 'cancelada'
            motivo_cancelacion = "El especialista ha marcado el día como no laborable."
            cita.descripcioncancelado = motivo_cancelacion
            
            # Recuperar al paciente para obtener su email
            paciente = User.query.get(cita.fkidusuario)
            
            if paciente and paciente.email:
                try:
                    send_email(
                        subject="Cancelación de Cita - MindCare",
                        recipients=[paciente.email],
                        template_name="aviso_cancelacion", # Nombre del archivo HTML sin .html (según tu mail_utils)
                        usuario=paciente,
                        cita=cita,
                        motivo=motivo_cancelacion
                    )
                    print(f"Correo enviado a {paciente.email}")
                except Exception as mail_error:
                    print(f"Error enviando correo a {paciente.email}: {mail_error}")
                    # No detenemos el proceso si falla un correo, solo lo logueamos
            
            count_canceladas += 1
        # -----------------------------------------------

        # 2. CREAR LA "AUTOCITA" DE BLOQUEO (Tu código sigue igual aquí)
        bloqueo_existente = Cita.query.filter_by(
            fkidpsicologo=user_id, 
            fkidusuario=user_id, 
            fecha=fecha_bloqueo,
            estado='aceptada'
        ).first()

        if not bloqueo_existente:
            nuevo_bloqueo = Cita(
                fkidusuario=user_id,
                fkidpsicologo=user_id,
                fecha=fecha_bloqueo,
                horainicio=time(0, 0),
                horafin=time(23, 59),
                estado='aceptada',
                descripcioncancelado='DIA_INHABIL'
            )
            db.session.add(nuevo_bloqueo)

        db.session.commit()

        return jsonify({
            'message': 'Día bloqueado y correos enviados', 
            'canceladas': count_canceladas
        }), 200

    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({'error': 'Error interno al bloquear día'}), 500

