# -*- coding: utf-8 -*-
"""User models."""
import datetime
import json
from uuid import uuid4

from xgaming.utils import RedisJsonModel


class User(RedisJsonModel):
    def __init__(self, *args, **kwargs):
        fields = {
            'email': u'',
            'key': 'email',
            'password': u'',
            'real_wallet_balance': 0.0,
            'bonus_wallet_balance': 0.0,
            'transactions': [],
            'created_date': None,
            'updated_date': None,
            'last_login_date': None
        }
        fields.update(kwargs)
        super(User, self).__init__(self, connection='REDIS_USER', **fields)

    def set_last_login(self):
        self.storage.execute_command('JSON.SET', self['email'], 'last_login_date',
                                     '"{}"'.format(str(datetime.datetime.now())))

    def save(self):
        try:
            data = self.data.copy()
            key = data.pop(data['key'])
            data['updated_date'] = datetime.datetime.now()
            if not data.get('created_date'):
                data['created_date'] = datetime.datetime.now()

            if len(data['password']) < 60:
                data['password'] = self.generate_password_hash(data['password'], 12).decode()
            self.storage.execute_command('JSON.SET', key, '.', json.dumps(data, default=str))
            return True
        except:
            raise

    def check_pass(self, password):
        return self.check_password_hash(self.get('password'), password.encode('utf-8'))

    def get_id(self):
        return self.get('email')

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False


class Bonus(RedisJsonModel):
    def __init__(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        """
        fields = {
            'id': uuid4().hex,
            'key': 'id',
            'type': u'',
            'amount': 0.0,
            'bonus': 0.0,
            'wallet': 1,
            'created_date': None,
            'updated_date': None
        }
        fields.update(kwargs)
        super(Bonus, self).__init__(self, connection='REDIS_CONFIG', **fields)
