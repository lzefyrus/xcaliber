# -*- coding: utf-8 -*-
"""Public forms."""
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired

from xgaming.user.models import User


class LoginForm(FlaskForm):
    """Login form."""

    email = StringField('E-Mail', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(LoginForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        """Validate the form."""
        initial_validation = super(LoginForm, self).validate()
        if not initial_validation:
            return False

        self.user = User(email=self.email.data).load(True)
        if not self.user:
            self.email.errors.append('Unknown email')
            return False

        if not self.user.check_pass(self.password.data):
            self.password.errors.append('Invalid password')
            return False
        return True
