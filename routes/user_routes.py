from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from functools import wraps
from models.user import db, User
from forms import RegisterForm, LoginForm, EditProfileForm

user_bp = Blueprint('user', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Debes iniciar sesión para acceder.', 'error')
            return redirect(url_for('user.login'))
        return f(*args, **kwargs)
    return decorated_function

@user_bp.route('/')
def user_list():
    users = User.query.all()
    return render_template('user_list.html', users=users)

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter((User.username == form.username.data) | (User.email == form.email.data)).first()
        if existing_user:
            flash('El usuario o correo ya existe.', 'error')
            return render_template('register.html', form=form)
        new_user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Registro exitoso. Por favor inicia sesión.', 'success')
        return redirect(url_for('user.login'))
    return render_template('register.html', form=form)

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data, password=form.password.data).first()
        if user:
            session['user_id'] = user.id
            session['username'] = user.username
            flash(f'Bienvenido {user.username}', 'success')
            return redirect(url_for('user.user_list'))
        else:
            flash('Usuario o contraseña incorrectos.', 'error')
    return render_template('login.html', form=form)

@user_bp.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada correctamente.', 'success')
    return redirect(url_for('user.login'))

@user_bp.route('/profile')
@user_bp.route('/profile/')
@login_required
def profile(id=None):
    if id is None:
        id = session.get('user_id')
    user = User.query.get_or_404(id)
    return render_template('profile.html', user=user)

@user_bp.route('/profile/edit')
@user_bp.route('/profile//edit', methods=['GET', 'POST'])
@login_required
def edit_profile(id=None):
    if id is None:
        id = session.get('user_id')
    user = User.query.get_or_404(id)
    form = EditProfileForm(obj=user)
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        db.session.commit()
        flash('Perfil actualizado con éxito.', 'success')
        return redirect(url_for('user.profile', id=user.id))
    return render_template('edit_profile.html', form=form, user=user)

@user_bp.route('/profile/delete', methods=['POST'])
@user_bp.route('/profile//delete', methods=['POST'])
@login_required
def delete_user(id=None):
    if id is None:
        id = session.get('user_id')
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    if session.get('user_id') == id:
        session.clear()
    flash('Usuario eliminado.', 'success')
    return redirect(url_for('user.user_list'))