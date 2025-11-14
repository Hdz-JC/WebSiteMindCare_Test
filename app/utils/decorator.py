# app/utils/decorators.py
from functools import wraps
from flask import g, redirect, url_for, flash, abort

def login_required(view):
    """
    Decorador que requiere que el usuario esté logueado para acceder a la vista.
    Redirige a la página de login si no está logueado.
    """
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            flash('Debes iniciar sesión para poder agendar citas.', 'warning')
            return redirect(url_for('user_bp.inicio')) # Redirige a tu ruta de login
        return view(*args, **kwargs)
    return wrapped_view

def role_required(required_roles):
    """
    Decorador que requiere que el usuario tenga uno de los roles especificados
    para acceder a la vista.
    Acepta un rol o una lista de roles.
    """
    if not isinstance(required_roles, list):
        required_roles = [required_roles]

    def decorator(view):
        @wraps(view)
        def wrapped_view(*args, **kwargs):
            if g.user is None:
                flash('Debes iniciar sesión para acceder a esta página.', 'warning')
                return redirect(url_for('user.inicio'))

            # Asumiendo que g.user tiene un atributo 'role' que es una instancia de RoleEnum
            if g.user.role.name not in [r.name if hasattr(r, 'name') else r for r in required_roles]:
                flash('No tienes permiso para acceder a esta página.', 'danger')
                # O podrías redirigir a una página de "Acceso Denegado"
                abort(403) # Lanza un error 403 Forbidden
            return view(*args, **kwargs)
        return wrapped_view
    return decorator