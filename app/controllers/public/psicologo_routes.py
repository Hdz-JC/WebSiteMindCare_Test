from flask import Blueprint, jsonify
from app.services.impl.psicologo_service_impl import PsicologoServiceImpl

psicologo_bp = Blueprint('psicologo_bp', __name__)
psicologo_service = PsicologoServiceImpl()

@psicologo_bp.route('/api/psicologo', methods=['GET'])
def obtener_psicologo():
    """Devuelve el primer psicólogo disponible"""
    data = psicologo_service.obtener_psicologo()
    status = 200 if "error" not in data else 404
    return jsonify(data), status

@psicologo_bp.route('/api/psicologos', methods=['GET'])
def listar_psicologos():
    """Devuelve la lista completa de psicólogos"""
    data = psicologo_service.listar_psicologos()
    status = 200 if "error" not in data else 400
    return jsonify(data), status
