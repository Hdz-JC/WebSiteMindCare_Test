from os import error
from flask import Blueprint, render_template, request, redirect, url_for, flash,session
from flask_migrate import show
from app.services.auth_service import authenticate_user,register_user
from datetime import datetime


main_bp = Blueprint ('main_bp',__name__)

#Rutas para archivos principales
@main_bp.route('/')
def inicio():
    return render_template('public/inicio.html')

@main_bp.route('/agendar')
def agendar():
    return render_template('public/agendar.html')

@main_bp.route('/quienesSomos')
def quienesSomos():
    return render_template('public/quienesSomos.html')

@main_bp.route('/ubicacion')
def ubicacion():
    return render_template('public/ubicacion.html')

@main_bp.route('/login', methods=['GET','POST'])
def login():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = authenticate_user(email, password)

        if user:
            session['user_id'] = user.id
            session['user_email'] = user.email
            session['user_nombre'] = f"{user.nombre}"
            flash('Inicio de sesion exitoso', 'Success')
            return redirect(url_for('main_bp.inicio'))
        else:
            flash('Correo o password incorrectos','danger')
            return render_template('public/inicio.html', email='', password='')


   # return render_template('components/login_modal.html')

#Todo el show
@main_bp.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada correctamente', 'success')
    return redirect(url_for('main_bp.inicio'))


@main_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    from app.models.user_model import RoleEnum
    
    if request.method == 'POST':
        email = request.form['email']
        
        try:
            # Captura de datos del formulario
            paterno = request.form['paterno']
            materno = request.form.get('materno')  # opcional
            nombre = request.form['nombre']
            edad = request.form.get('edad')
            fecha_nacimiento = request.form.get('fecha_nacimiento')
            sexo = request.form.get('sexo')
            direccion = request.form.get('direccion')
            celular = request.form.get('celular')
            email = request.form['email']
            password = request.form['password']
            role=RoleEnum.paciente

            # Llamar al service
            user, errores = register_user(
                paterno=paterno,
                materno=materno,
                nombre=nombre,
                fecha_nacimiento=fecha_nacimiento,
                sexo=sexo,
                direccion=direccion,
                celular=celular,
                email=email,
                password=password
            )

            if not user:
                for e in errores:
                    if e == "email":
                        flash("El correo ya está registrado.", "warning")
                    elif e == "celular":
                        flash("El número de celular ya está registrado.", "warning")
                return render_template("public/registro.html")
            flash('Registro exitoso. Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('main_bp.inicio'))
       
       
        except Exception as e:
            from app.models import db
            db.session.rollback()
            flash(f'Error al registrar usuario', 'danger')
            print({str(e)})
            return render_template('public/registro.html')

    # GET → renderiza el formulario
    return render_template('public/registro.html')