# app/controllers/public/user_routes.py (anteriormente user_controller.py)
from flask import Blueprint, render_template, request, redirect, url_for,jsonify, flash, session,g
from app.validators.user_validator import UserValidator

# Importaciones CORRECTAS para los servicios
from app.services.impl.user_service_impl import UserServiceImpl
from app.services.auth.auth_service import AuthService
# Para el rol en el registro

from app.utils.decorator import login_required

user_bp = Blueprint('user_bp', __name__)

# --- Instanciación de los servicios ---
# Esto podría mejorarse con un patrón de inyección de dependencias más avanzado
# pero para una app Flask simple, esto funciona.
user_service = UserServiceImpl()
auth_service = AuthService(user_service) # Inyectamos user_service en auth_service

# ------------------------------------

# Rutas para archivos principales
@user_bp.route('/')
def inicio():
    return render_template('public/inicio.html')

@user_bp.route('/agendar')
@login_required
def agendar():
    return render_template('paciente/agendar.html',user=g.user)

@user_bp.route('/quienesSomos')
def quienesSomos():
    return render_template('public/quienesSomos.html')

@user_bp.route('/ubicacion')
def ubicacion():
    return render_template('public/ubicacion.html')

# 🟢 LOGIN
@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # 🔹 Soporta JSON y formulario HTML
        data = request.get_json(silent=True) or request.form

        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            if request.is_json:
                return jsonify({'error': 'Email y contraseña son requeridos'}), 400
            flash('Email y contraseña son requeridos', 'warning')
            return render_template('public/inicio.html', email=email)

        user = auth_service.login(email, password)

        if user:
            session['user_id'] = user.id
            session['user_email'] = user.email
            session['user_nombre'] = user.nombre

            if request.is_json:
                return jsonify({
                    'message': 'Inicio de sesión exitoso',
                    'user': {
                        'id': user.id,
                        'nombre': user.nombre,
                        'email': user.email
                    }
                }), 200

            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('user_bp.inicio'))
        else:
            if request.is_json:
                return jsonify({'error': 'Correo o contraseña incorrectos'}), 401

            flash('Correo o contraseña incorrectos', 'danger')
            return render_template('public/inicio.html', email=email)

    # GET
    if request.is_json:
        return jsonify({'message': 'Método GET no permitido para login'}), 405
    return render_template('public/inicio.html')


# 🟢 LOGOUT
@user_bp.route('/logout', methods=['GET'])
def logout():
    session.clear()

    if request.is_json:
        return jsonify({'message': 'Sesión cerrada correctamente'}), 200

    flash('Sesión cerrada correctamente', 'success')
    return redirect(url_for('user_bp.inicio'))


# 🟢 REGISTRO
@user_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        data = request.get_json(silent=True) or request.form

        errores = UserValidator.validate_registration(data)
        if errores:
            if request.is_json:
                return jsonify({'errores': errores}), 400
            for e in errores:
                flash(e, "warning")
            return render_template("public/registro.html", **data)

        errores = UserValidator.check_duplicates(data)
        if errores:
            if request.is_json:
                return jsonify({'errores': errores}), 400
            for e in errores:
                flash(e, "warning")
            return render_template("public/registro.html", **data)

        try:
            paterno = data.get('paterno')
            materno = data.get('materno')
            nombre = data.get('nombre')
            edad = data.get('edad')
            fecha_nacimiento = data.get('fecha_nacimiento')
            sexo = data.get('sexo')
            direccion = data.get('direccion')
            celular = data.get('celular')
            email = data.get('email')
            raw_password = data.get('password')

            user, errores_servicio = auth_service.register(
                paterno=paterno,
                materno=materno,
                nombre=nombre,
                edad=edad,
                fecha_nacimiento=fecha_nacimiento,
                sexo=sexo,
                direccion=direccion,
                celular=celular,
                email=email,
                raw_password=raw_password
            )

            if errores_servicio:
                if request.is_json:
                    return jsonify({'errores': errores_servicio}), 400
                for e in errores_servicio:
                    flash(f"Error: {e}", "warning")
                return render_template("public/registro.html", **data)

            if request.is_json:
                return jsonify({'message': 'Registro exitoso', 'user': {'email': email}}), 201

            flash('Registro exitoso. ¡Ya puedes iniciar sesión!', 'success')
            return redirect(url_for('user_bp.inicio'))

        except Exception as e:
            from app.models import db
            db.session.rollback()
            if request.is_json:
                return jsonify({'error': f'Error al registrar usuario: {str(e)}'}), 500
            flash(f'Error al registrar usuario: {e}', 'danger')
            return render_template('public/registro.html', **data)

    # GET
    if request.is_json:
        return jsonify({'message': 'Método GET no permitido para registro'}), 405
    return render_template('public/registro.html')