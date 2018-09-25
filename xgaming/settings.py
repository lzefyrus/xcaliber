# -*- coding: utf-8 -*-
"""Application configuration.

Most configuration is set via environment variables.

For local development, use a .env file to set
environment variables.
"""
import datetime

from environs import Env

env = Env()
env.read_env()

ENV = env.str('FLASK_ENV', default='production')
DEBUG = ENV == 'development'
SECRET_KEY = env.str('SECRET_KEY')
BCRYPT_LOG_ROUNDS = env.int('BCRYPT_LOG_ROUNDS', default=13)
DEBUG_TB_ENABLED = DEBUG
DEBUG_TB_INTERCEPT_REDIRECTS = False
CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.
WEBPACK_MANIFEST_PATH = 'webpack/manifest.json'
REDIS_USER_URL = 'redis://localhost:6379/1'
REDIS_WALLET_URL = 'redis://localhost:6379/2'
REDIS_CONFIG_URL = 'redis://localhost:6379/0'
BONUS = [{'id': '51eb21f94a654814bf818d7d3d212073', 'key': 'id', 'type': 'deposit', 'amount': 100.0, 'wallet': 1,
          'bonus': 20.0, 'created_date': datetime.datetime(2018, 9, 24, 4, 47, 31, 818146), 'updated_date': None},
         {'id': '7e59ab504a804bafa948145971237696', 'key': 'id', 'type': 'login', 'amount': 0.0, 'wallet': 0,
          'bonus': 100.0, 'created_date': datetime.datetime(2018, 9, 24, 4, 45, 31, 722004), 'updated_date': None}]
