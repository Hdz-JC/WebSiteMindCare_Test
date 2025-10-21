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
@main_bp.route('/registro')
def registro():
    return render_template('public/registro.html')

#Registro
@main_bp.route('/api/register', methods=['POST'])
def api_register():
    data = request.form
    if not data:
        return jsonify({'error': 'No JSON body received'}), 400

    email = data.get('email')
    password = data.get('password')
    nombre = data.get('nombre')
    paterno = data.get('paterno')
    materno = data.get('materno')
    fecha_nacimiento = data.get('fecha_nacimiento')
    sexo = data.get('sexo')
    direccion = data.get('direccion')
    celular = data.get('celular')
    
    try:
        user = User(
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

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error al crear usuario', 'detail': str(e)}), 500

    return jsonify({'message': 'Usuario creado', 'user_id': user.id}), 201
