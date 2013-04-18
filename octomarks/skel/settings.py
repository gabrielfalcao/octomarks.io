# -*- coding: utf-8; mode: python -*-
import os
from os.path import join, abspath

LOCAL_PORT = 5000
PORT = os.getenv('PORT', LOCAL_PORT)

# READY TO DEPLOY
DEBUG = PORT is LOCAL_PORT
PRODUCTION = not DEBUG

# Session key, CHANGE IT IF YOU GET TO THE PRODUCTION! :)
SECRET_KEY = 'P4wned!'

# Database connection URI
DATABASE = "sqlite:///../data/yourproject.sqlite"

# Static assets craziness
LOCAL_FILE = lambda *p: abspath(join(__file__, '..', *p))

COMPASS_CONFIG = dict(
    http_path='/',
    css_dir='css',
    sass_dir='sass',
    images_dir='img',
    javascripts_dir='js',
    generated_images_dir='./',
    http_generated_images_path='/static',
    http_images_path='/static',
    sprite_load_path=[
        # LOCAL_FILE('static', 'img'),
    ],
    additional_import_paths=[
        # LOCAL_FILE('static', 'sass'),
    ]
)
SQLALCHEMY_DATABASE_URI = DATABASE


if DEBUG:  # localhost
    GITHUB_CONSUMER_KEY = 'localhost:{0}-consumer-key'.format(PORT)
    GITHUB_ACCESS_TOKEN_URL = 'localhost:{0}-access-token-url'.format(PORT)
    DOMAIN = 'localhost:{0}'.format(PORT)

else:
    GITHUB_CONSUMER_KEY = 'app-name-consumer-key'
    GITHUB_ACCESS_TOKEN_URL = 'app-name-access-token-url'
    DOMAIN = 'app-name.herokuapp.com'

SCHEMA = 'http://'

absurl = lambda *path: "{0}{1}/{2}".format(SCHEMA, DOMAIN, "/".join(path))
