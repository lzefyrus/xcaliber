# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint
from flask_login import login_required

blueprint = Blueprint('wallet', __name__, url_prefix='/wallet', static_folder='../static')


@blueprint.route('/')
@login_required
def wallet_funds():
    """List members."""
    pass
