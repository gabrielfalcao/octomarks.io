# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from glob import glob
from os.path import split

from octomarks.ui import ThemeManager
from octomarks import settings

L = settings.LOCAL_FILE


each_filename = lambda path: split(path)[-1]
theme_file = lambda filename: L('static', 'themes', filename)
enumerate_themes = lambda name: map(each_filename, glob(theme_file(name)))


def test_theme_manager_lists_exising_themes():
    "ThemeManager should be able to find themes under /static/themes"

    expected_files = enumerate_themes('*.css')

    ThemeManager.get_theme_files().should.equal(expected_files)


def test_load_theme_by_filename():
    "ThemeManager should be able to load themes by filename"

    path = theme_file('github.css')

    with open(path) as theme:
        ThemeManager.load_theme('github.css').should.equal({
            'name': 'github',
            'path': path,
            'content': theme.read()
        })


def test_load_theme_by_theme_name():
    "ThemeManager should be able to load themes by name"

    path = theme_file('github.css')

    with open(path) as theme:
        ThemeManager.load_theme('github').should.equal({
            'name': 'github',
            'path': path,
            'content': theme.read()
        })
