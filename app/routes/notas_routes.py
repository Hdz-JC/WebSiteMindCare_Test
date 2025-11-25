from flask import Blueprint, jsonify, request, g
from app.utils.decorator import login_required, role_required
from app.services.impl.notas_service_impl import NotasServiceImpl 

notas_bp = Blueprint('notas_bp', __name__)
notas_service = NotasServiceImpl()


# OBTENER NOTAS DE UN USUARIO
@notas_bp.route("/api/notas/<int:idusuario>", methods=["GET"])
@login_required
def obtener_notas(idusuario):
    notas = notas_service.obtener_notas_por_usuario(idusuario)
    return jsonify(notas), 200



# AGREGAR NOTA
@notas_bp.route("/api/notas/agregar", methods=["POST"])
@login_required
def agregar_nota():

    data = request.get_json()
    idcita = data.get("idcita")
    contenido = data.get("contenido")
    titulo = data.get("titulo")

    if not idcita or not contenido or not titulo:
        return jsonify({"error": "Faltan datos"}), 400

    try:
        # Convertimos idcita a int por seguridad
        notas_service.agregar_nota(int(idcita), contenido, g.user, titulo)
        return jsonify({"message": "Nota registrada"}), 200

    except PermissionError:
        return jsonify({"error": "Sin permisos"}), 403

    except Exception as e:
        print("→ ERROR GENERAL:", e)
        return jsonify({"error": str(e)}), 500


