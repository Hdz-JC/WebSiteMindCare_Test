
from flask import Blueprint, render_template, jsonify
from datetime import date, datetime
from app.models import db, Cita, User
from app.utils.decorator import role_required, login_required

monitor_bp = Blueprint('monitor_bp', __name__, template_folder='templates')

# Página visual (HTML)

@monitor_bp.route('/monitor')
@login_required
@role_required('general')
def monitor_pacientes_hoy():
    """Vista pública para mostrar pacientes a atender hoy"""
    hoy = date.today()
    # Traer citas de hoy que no estén canceladas, ordenadas por hora inicio
    rows = (
        db.session.query(Cita, User)
        .join(User, User.id == Cita.fkidusuario)
        .filter(Cita.fecha == hoy, Cita.estado != 'cancelada')
        .order_by(Cita.horainicio)
        .all()
    )

    # Convertir para la plantilla: lista de dicts
    usuarios = []
    for cita, usuario in rows:
        usuarios.append({
            "idcita": cita.idcita,
            "nombre": f"{usuario.nombre} {usuario.paterno} {usuario.materno or ''}".strip(),
            # formatear hh:mm
            "hora_inicio": cita.horainicio.strftime("%H:%M"),
            "hora_fin": cita.horafin.strftime("%H:%M"),
            "fecha": cita.fecha.strftime("%Y-%m-%d")
        })

    return render_template('monitor/today_monitor.html', usuarios=usuarios, hoy=hoy.strftime("%d/%m/%Y"))


# API JSON para actualizaciones en tiempo real

@monitor_bp.route('/api/monitor/today', methods=['GET'])
@login_required
@role_required('general')
def api_monitor_today():
    hoy = date.today()
    rows = (
        db.session.query(Cita, User)
        .join(User, User.id == Cita.fkidusuario)
        .filter(Cita.fecha == hoy, Cita.estado != 'cancelada')
        .order_by(Cita.horainicio)
        .all()
    )

    resultados = []
    for cita, usuario in rows:
        resultados.append({
            "idcita": cita.idcita,
            "nombre": f"{usuario.nombre} {usuario.paterno} {usuario.materno or ''}".strip(),
            "hora_inicio": cita.horainicio.strftime("%H:%M"),
            "hora_fin": cita.horafin.strftime("%H:%M"),
            "fecha": cita.fecha.strftime("%Y-%m-%d")
        })

    return jsonify(resultados), 200
