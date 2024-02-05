from flask import (
    Blueprint, render_template, request, url_for, redirect, flash, session, g
    )

from werkzeug.security import generate_password_hash, check_password_hash

from .models import User
from todor import db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/get_users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = [{'id': user.id, 'username': user.username} for user in users]
    return {'users': user_list}



@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Verifica si ya hay usuarios en la base de datos
        if User.query.count() == 0:
            rol = 'admin'
        else:
            rol = 'user'

        user = User(username=username, rol=rol, password=generate_password_hash(password))

        error = None

        user_name = User.query.filter_by(username=username).first()
        if user_name is None:
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            error = f'El usuario {username} ya está registrado'
        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods= ('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        
        user = User.query.filter_by(username=username).first()

        if user is None or not check_password_hash(user.password, password):
            error = 'Usuario o contraseña incorrectos'

        
        #iniciar sesion
        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('todo.index'))
        flash(error)
    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get_or_404(user_id)

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))



import functools

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view