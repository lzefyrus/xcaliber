# -*- coding: utf-8 -*-
"""User forms."""
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange

from .models import User


class RegisterForm(FlaskForm):
    """Register form."""

    email = StringField('Email',
                        validators=[DataRequired(), Email(), Length(min=6, max=40)])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=2, max=40)])
    confirm = PasswordField('Verify password',
                            [DataRequired(), EqualTo('password', message='Passwords must match')])

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        """Validate the form."""
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User(email=self.email.data, key='email').load(True)
        if user.get('created_date'):
            self.username.errors.append('Email already registered')
            return False
        return True


class ChargeForm(FlaskForm):
    charge = IntegerField('Charge', validators=[DataRequired(message='You must add at least 1 EURO'),
                                                NumberRange(min=1, max=10000, message="You must add at least 1 EURO ")])

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(ChargeForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(ChargeForm, self).validate()
        if not initial_validation:
            return False
        try:
            charge_amount = int(self.charge.data)
            if charge_amount < 1:
                self.charge.errors.append('You must add at least 1 EURO')
                return False
        except ValueError:
            self.charge.errors.append('You must add at least 1 EURO')
            return False
        return True
