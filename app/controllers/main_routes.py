from flask import Blueprint, render_template

main_bp = Blueprint ('main_bp',__name__)

#Rutas para archivos principales
@main_bp.route('/')
def inicio():
    return render_template('inicio.html')

@main_bp.route('/citas')
def citas():
    return render_template('citas.html')

@main_bp.route('/quienesSomos')
def quienesSomos():
    return render_template('quienesSomos.html')

@main_bp.route('/ubicacion')
def ubicacion():
    return render_template('ubicacion.html')

@main_bp.route('/login')
def login():
    return render_template('login.html')


