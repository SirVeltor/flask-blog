from flask import Flask, url_for, render_template, request, redirect
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import login_manager
from . import auth_bp
from .forms import SingupForm, LoginForm
from .models import User


@auth_bp.route('/signup/', methods=['GET', 'POST'])
def show_signup_form():
    form = SingupForm()
    error_message = ''
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data

        user = User.get_by_email(email)


        if user is not None:
            error_message = f'El email {email} ya está siendo utilizado por otro usuario'
        else:
            user = User(name=name, email=email)
            user.set_password(password)
            user.save()

            login_user(user, remember=True)
            next = request.args.get('next', None)

            if next:
                return redirect(next)
            print('name -->', name, '\n email -->', email, '\n password -->', password)
            return redirect(url_for('public.index'))
    return render_template('auth/signup_form.html', form=form, error=error_message)


@auth_bp.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_email(form.email.data)
        print('password -->', form.password.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                return redirect(url_parse('index'))
            else:
                return redirect(next_page)
        else:
            data = {'form': form, 'message': 'Usuario no encontrado'}
            return render_template('auth/login_form.html', form=data)
    data = {'form': form}
    return render_template('auth/login_form.html', form=data)


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('public.index'))


@login_manager.user_loader
def load_user(user_id):
    print('Ejecutando load_user !!! -->', user_id)
    return User.get_by_id(int(user_id))