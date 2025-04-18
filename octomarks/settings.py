# -*- coding: utf-8; mode: python -*-
import os
from uuid import uuid4
from os.path import join, abspath

LOCAL_PORT = 5000
PORT = os.getenv('PORT', LOCAL_PORT)

# READY TO DEPLOY
DEBUG = PORT is LOCAL_PORT
PRODUCTION = not DEBUG

# Database connection URI
DATABASE = 'mysql://gbookmarks:b00k@BABY@mysql.gabrielfalcao.com/gbookmarks'

if not PRODUCTION:
    DATABASE = os.getenv('OCTOMARKS_DB', 'mysql://root@localhost/gb')

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
    GITHUB_CLIENT_ID = '33a3775824b15fbefc70'
    GITHUB_CLIENT_SECRET = '67f286a7c7c234e0b1014155409d3f07892932ad'
    DOMAIN = 'localhost:{0}'.format(PORT)

else:
    GITHUB_CLIENT_ID = '491daa32a3fffba61846'
    GITHUB_CLIENT_SECRET = '427e42629007fa7227bf1f23a48d216cda904d50'
    DOMAIN = 'octomarks.io'

SCHEMA = 'http://'

absurl = lambda *path: "{0}{1}/{2}".format(SCHEMA, DOMAIN, "/".join(path).lstrip('/'))

RELEASE = os.getenv('RELEASE', uuid4().hex)
# Session key, CHANGE IT IF YOU GET TO THE PRODUCTION! :)
SECRET_KEY = RELEASE + '%F&G*&H(*ds3657d468f57g68h'
