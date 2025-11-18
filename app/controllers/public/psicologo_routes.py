from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify, flash
from app.services.impl.psicologo_service_impl import PsicologoServiceImpl
from app.utils.decorator import login_required
from datetime import date, datetime, timezone
from app.models import Cita, User
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
def inicio_psicologo():
    if session.get('user_rol') != 'psicologo':
        return redirect(url_for('user_bp.inicio'))
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
    
    return render_template('psicologo/expedientes_paciente.html', rol='psicologo')

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

    return render_template('psicologo/notas_paciente.html', rol='psicologo', cita=cita, paciente=paciente)