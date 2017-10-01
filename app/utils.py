from flask import session, flash, request, url_for

from .models import *


def get_current_user():
    if session.get('logged_in'):
        return User.get(User.username == session.get('username'))


def auth_user(user, remember=False):
    session['logged_in'] = True
    session['username'] = user.username
    flash("You are log in as {}".format(session['username']))
    session['permanent'] = remember


def redirect_url(default='.index'):
    return request.args.get('next') or \
           request.referrer or \
           url_for(default)
