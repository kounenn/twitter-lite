from flask import render_template, session, redirect, url_for, flash

from app.decorators import login_required
from . import auth
from .forms import RegisterForm, LoginForm, ChangePasswordForm
from ..models import User
from ..utils import auth_user, get_current_user


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('logged_in'):
        flash('You have been logged in')
        redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.get(User.email == form.email.data)
        except User.DoesNotExist:
            flash('Email Address does not exist')
        else:
            if user.verify_password(form.password.data):
                auth_user(user, form.remember_me.data)
                return redirect(url_for('main.index'))
            flash('Invalid username or password')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    session['logged_in'] = False
    flash('You have been logged out')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # form has been handle possible conflict of new entry
        user = User()
        user.username = form.username.data
        user.email = form.email.data
        user.password = form.password.data
        user.save()
        auth_user(user, form.remember_me.data)
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)


@auth.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        user = get_current_user()
        password = form.old_password.data
        if user.verify_password(password):
            user.password = form.new_password.data
            user.save()
            flash('Your password has been update')
            return redirect(url_for('main.index'))
        flash('Invalid password')
    return render_template('auth/change_password.html', form=form)
