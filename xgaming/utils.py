# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""
import datetime
import json
from _collections_abc import Mapping
from collections import UserDict

from flask import flash, current_app
from flask_bcrypt import check_password_hash, generate_password_hash
from redis import ConnectionError


def flash_errors(form, category='warning'):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash('{0} - {1}'.format(getattr(form, field).label.text, error), category)


def show_slots(slots=[]):
    for s in slots:
        flash(s, 'slot')


class RedisJsonModel(UserDict):
    storage = None
    is_dirty = False

    def __init__(self, *args, connection=None, **kwargs):
        # print(kwargs)
        super(RedisJsonModel, self).__init__(**kwargs)
        redis = current_app.extensions['redis']

        if connection in redis.keys():
            self.storage = redis[connection]
            self.check_password_hash = check_password_hash
            self.generate_password_hash = generate_password_hash
        else:
            raise ConnectionError

    def __setitem__(self, key, item):
        self.data[key] = item
        self.is_dirty = True

    def update(*args, **kwds):
        ''' D.update([E, ]**F) -> None.  Update D from mapping/iterable E and F.
            If E present and has a .keys() method, does:     for k in E: D[k] = E[k]
            If E present and lacks .keys() method, does:     for (k, v) in E: D[k] = v
            In either case, this is followed by: for k, v in F.items(): D[k] = v
        '''
        if not args:
            raise TypeError("descriptor 'update' of 'MutableMapping' object "
                            "needs an argument")
        self, *args = args
        if len(args) > 1:
            raise TypeError('update expected at most 1 arguments, got %d' %
                            len(args))
        if args:
            other = args[0]
            if isinstance(other, Mapping):
                for key in other:
                    self[key] = other[key]
            elif hasattr(other, "keys"):
                for key in other.keys():
                    self[key] = other[key]
            else:
                for key, value in other:
                    self[key] = value
        for key, value in kwds.items():
            self[key] = value

        self.is_dirty = True

    def save(self):
        try:
            data = self.data.copy()
            key = data.pop(data['key'])
            self.storage.execute_command('JSON.SET', key, '.', json.dumps(data, default=str))
            self.is_dirty = False
            return self
        except:
            raise

    def load(self, silent=True):
        if any(('key' not in self.keys(),
                self.get(self['key']) is False)):
            if silent:
                raise Exception('key and value key KEYs are required to load data')

        try:
            data = self.storage.execute_command('JSON.GET', self[self['key']])

            if not data:
                return self

            for k, w in json.loads(data).items():
                if k[-4:] == 'date':
                    try:
                        self[k] = datetime.datetime.strptime(w, "%Y-%m-%d %H:%M:%S.%f")
                    except Exception:
                        self[k] = w
                else:
                    self[k] = w
            self.is_dirty = False
            return self
        except:
            raise

    def load_all(self, keys=None, skip_dates=False):
        """
        gets records from keys
        :param keys: ['', '']
        :return: [{},{}]
        """
        if keys is None:
            keys = list(i.decode() for i in self.storage.keys('*'))

        objs = []

        for k in keys:
            data = self.storage.execute_command('JSON.GET', k)
            for item in data:
                tmp = self.copy()
                for k, w in json.loads(data).items():
                    if k[-4:] == 'date' and skip_dates is False:
                        tmp[k] = datetime.datetime.strptime(w, "%Y-%m-%d %H:%M:%S.%f")
                    else:
                        tmp[k] = w
                tmp.is_dirty = False
            objs.append(tmp)

        return objs
