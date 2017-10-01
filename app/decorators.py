from functools import wraps

from flask import session, redirect, flash, url_for


def login_required(f):
    @wraps(f)
    def inner(*args, **kwargs):
        if not session.get('logged_in'):
            flash('You must be logged in')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)

    return inner
