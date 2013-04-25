# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import codecs
from glob import glob
from os.path import split, splitext

from octomarks import settings
L = settings.LOCAL_FILE


each_filename = lambda path: split(path)[-1]
theme_file = lambda filename: L('static', 'themes', filename)
enumerate_themes = lambda name: map(each_filename, glob(theme_file(name)))


class ThemeManager(object):
    @classmethod
    def get_theme_files(self):
        return enumerate_themes('*.css')

    @classmethod
    def load_theme(self, filename):
        if not filename.endswith('.css'):
            filename = "{0}.css".format(filename)

        path = theme_file(filename)
        with codecs.open(path, 'r', 'utf-8') as theme:
            content = theme.read()

        return {
            'name': splitext(filename)[0],
            'path': path,
            'content': content,
        }
