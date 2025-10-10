from flask import Blueprint, render_template

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

@main_bp.route('/registro')
def registro():
    return render_template('public/registro.html')
