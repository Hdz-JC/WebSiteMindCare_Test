from flask import Blueprint, request, jsonify, g
from app.utils.decorator import login_required
from app.services.impl.citas_service_impl import CitaServiceImpl

citas_bp = Blueprint('citas_bp', __name__)
cita_service = CitaServiceImpl()

@citas_bp.route('/api/citas/listar', methods=['GET'])
@login_required
def listar_citas():
    """Devuelve todas las citas registradas (para mostrar en el calendario)"""
    citas = cita_service.obtener_citas()  # función que debes tener en tu service
    return jsonify(citas), 200



@citas_bp.route('/api/citas', methods=['POST'])
@login_required
def agendar_cita():
    """Crea una nueva cita para el usuario logueado"""
    data = request.get_json()

    # Validar datos mínimos
    if not all(k in data for k in ("fecha", "horainicio", "horafin")):
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    data["fkidusuario"] = g.user.id
    result = cita_service.agendar_cita(data)
    status = 200 if "error" not in result else 400
    return jsonify(result), status

