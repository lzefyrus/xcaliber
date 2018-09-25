# -*- coding: utf-8 -*-
"""User views."""
import random

from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from flask_login import login_required

from xgaming.utils import flash_errors, show_slots
from xgaming.wallet import models
from .forms import ChargeForm

blueprint = Blueprint('user', __name__, url_prefix='/users', static_folder='../static')


@blueprint.route('/', methods=['GET', 'POST'])
@login_required
def members():
    """List members."""
    form = ChargeForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            deposit = models.Wallet(amount=float(form.charge.data)).deposit()
            for bonus in session['bonus']:
                if bonus['type'] == 'deposit' and int(deposit['amount']) >= bonus['amount']:
                    models.Wallet(amount=bonus['bonus'], type=1, reference=deposit['guid']).deposit()
            if deposit:
                flash('You added {} to your wallet'.format(float(form.charge.data)), 'success')
                return redirect(url_for('user.members'))
        else:
            flash_errors(form)
    return render_template('users/members.html', form=form)


@blueprint.route('/spin', methods=['POST'])
@login_required
def spin():
    """Spins"""
    spin_amount = 2
    win = None
    spin = None
    w = 0
    for w in [0, 1]:
        if models.Wallet(amount=spin_amount, type=w).withdraw():
            win, spin = slot()
            break

    if not spin:
        flash('Please add some cash.', 'error')

    elif win is False:
        show_slots(spin)
        flash('Better luck next time', 'message')

    elif win is True:
        if models.Wallet(amount=spin_amount, type=w).deposit():
            show_slots(spin)
            flash('Congratulations', 'success')

    return redirect(url_for('user.members'))


def slot(dificulty=3):
    slots = ['bell',
             'bug',
             'bomb',
             'coffee',
             'diamond',
             'star']

    result = []

    for i in range(dificulty):
        result.append(random.choice(slots))

    return (len(set(result)) == 1), result
