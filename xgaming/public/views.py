# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import Blueprint, flash, redirect, render_template, request, url_for, session, current_app
from flask_login import login_required, login_user, logout_user, current_user

from xgaming.extensions import login_manager
from xgaming.public.forms import LoginForm
from xgaming.user.forms import RegisterForm
from xgaming.user.models import User, Bonus
from xgaming.utils import flash_errors
from xgaming.wallet import models

blueprint = Blueprint('public', __name__, static_folder='../static')


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User(email=user_id).load(False)


def add_base_bonus():
    for b in current_app.config.get('BONUS'):
        try:
            tmp = Bonus(**b).save()
        except Exception as e:
            print(e)


@blueprint.route('/', methods=['GET', 'POST'])
def home():
    """Home page."""
    form = LoginForm(request.form)
    # Handle logging in
    if request.method == 'POST':
        if form.validate_on_submit():
            add_base_bonus()
            login_user(form.user, force=True)
            current_user.set_last_login()
            a = Bonus().load_all(skip_dates=True)
            session['bonus'] = session_bonus(a)
            flash('You are logged in.', 'success')
            login_bonus()
            redirect_url = request.args.get('next') or url_for('user.members')
            return redirect(redirect_url)
        else:
            flash_errors(form)
    return render_template('public/home.html', form=form)


def login_bonus():
    for bonus in session['bonus']:
        if bonus['type'] == 'login':
            models.Wallet(amount=bonus['bonus'], type=0, reference=bonus['type']).deposit()


def session_bonus(bonus=[]):
    rte = []
    for b in bonus:
        rte.append(b.data)

    return rte


@blueprint.route('/logout/')
@login_required
def logout():
    """Logout."""
    logout_user()
    flash('You are logged out.', 'info')
    return redirect(url_for('public.home'))


@blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    """Register new user."""
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        User(email=form.email.data, password=form.password.data).save()
        flash('Thank you for registering. You can now log in.', 'success')
        return redirect(url_for('public.home'))
    else:
        flash_errors(form)
    return render_template('public/register.html', form=form)


@blueprint.route('/about/')
def about():
    """About page."""
    form = LoginForm(request.form)
    return render_template('public/about.html', form=form)
