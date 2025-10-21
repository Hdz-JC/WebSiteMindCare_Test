from flask import Blueprint, render_template, request, redirect, url_for, flash,session
from app.models.user_model import User, db

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

@main_bp.route('/login', methods=['GET','POST'])
def login():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email, password=password).first()

        if user:
            session['user_id'] = user.id
            session['user_email'] = user.email
            flash('Inicio de sesion exitoso', 'Success')
            return redirect(url_for('main_bp.inicio'))
        else:
            flash('Correo o password incorrectos','danger')
            return redirect(url_for('main_bp.ubicacion'))

    #return render_template('components/login_modal.html')

#Todo el show

@main_bp.route('/registro')
def registro():
    return render_template('public/registro.html')
