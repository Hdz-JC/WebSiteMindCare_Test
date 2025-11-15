from flask import Blueprint, render_template, session, redirect, url_for
from app.utils.decorator import login_required

psicologo_bp = Blueprint('psicologo_bp', __name__, url_prefix='/psicologo')

@psicologo_bp.route('/inicio')
@login_required
def inicio_psicologo():
    # Validar que el usuario sea psicólogo
    if session.get('user_rol') != 'psicologo':
        return redirect(url_for('user_bp.inicio'))

    return render_template('psicologo/inicio_psicologo.html', rol='psicologo')