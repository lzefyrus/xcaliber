# -*- coding: utf-8 -*-
"""User models."""
import datetime
from uuid import uuid4

from flask_login import current_user

from xgaming.utils import RedisJsonModel


class Wallet(RedisJsonModel):
    """
    0: real
    1: bonus
    """

    def __init__(self, *args, **kwargs):
        fields = {
            'guid': uuid4().hex,
            'key': 'guid',
            'amount': 0.0,
            'type': 0,
            'reference': u'',
            'created_date': datetime.datetime.now()
        }
        fields.update(kwargs)
        super(Wallet, self).__init__(self, connection='REDIS_WALLET', **fields)

    def wb(self):
        return 'real_wallet_balance' if self['type'] is 0 else 'bonus_wallet_balance'

    def withdraw(self):

        if self.get('amount', 0) > 0.0:
            self['amount'] = - self['amount']

        if current_user[self.wb()] + self['amount'] < 0:
            return False

        if (self.save()):
            pipe = current_user.storage.pipeline()
            pipe.execute_command('JSON.ARRAPPEND', '{}'.format(current_user['email']), 'transactions',
                                 '"{}"'.format(self['guid']))
            pipe.execute_command('JSON.NUMINCRBY', '{}'.format(current_user['email']), '{}'.format(self.wb()),
                                 int(self['amount']))
            pipe.execute()
        return self

    def deposit(self):
        if self.get('amount', 0) <= 0.0:
            return True

        if (self.save()):
            pipe = current_user.storage.pipeline()
            pipe.execute_command('JSON.ARRAPPEND', '{}'.format(current_user['email']), 'transactions',
                                 '"{}"'.format(self['guid']))
            pipe.execute_command('JSON.NUMINCRBY', '{}'.format(current_user['email']), '{}'.format(self.wb()),
                                 int(self['amount']))
            pipe.execute()
        return self
