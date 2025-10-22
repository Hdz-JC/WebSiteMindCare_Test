from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.models.user_model import User
from app import db
from datetime import datetime

main_bp = Blueprint ('main_bp',__name__)

#Rutas para archivos principales
@main_bp.route('/')
def inicio():
    return render_template('public/inicio.html')

@main_bp.route('/agendar')
def citas():
    return render_template('public/agendar.html')

@main_bp.route('/quienesSomos')
def quienesSomos():
    return render_template('public/quienesSomos.html')

@main_bp.route('/ubicacion')
def ubicacion():
    return render_template('public/ubicacion.html')

@main_bp.route('/login')
def login():
    return render_template('public/login.html')

#Todo el show de registro
@main_bp.route('/registro', methods=['GET','POST'])
def registro():
    if request.method == 'POST':
        try:
            # Captura de datos del formulario
            apPaterno = request.form['apPaterno']
            apMaterno = request.form['apMaterno']
            nombre = request.form['nombre']
            edad = int(request.form['edad'])
            fecha_nacimiento = datetime.now().date().replace(year=datetime.now().year - edad)
            sexo = request.form['sexo']
            direccion = request.form['direccion']
            estado = request.form.get('estado')  # opcional
            celular = request.form['celular']
            email = request.form['email']
            password = request.form['password']

            # Validación básica
            if User.query.filter_by(email=email).first():
                flash('El correo ya está registrado.', 'warning')
                return render_template('public/registro.html')

            # Creación del usuario usando el método personalizado
            user = User.create(
                paterno=apPaterno,
                materno=apMaterno,
                nombre=nombre,
                fecha_nacimiento=fecha_nacimiento,
                sexo=sexo,
                direccion=direccion,
                estado=estado,
                celular=celular,
                email=email,
                password=password
            )

            flash('Registro exitoso. Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('main_bp.login'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar usuario: {str(e)}', 'danger')
            return render_template('public/registro.html')

    return render_template('public/registro.html')