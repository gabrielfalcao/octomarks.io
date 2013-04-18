#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import wraps
from octomarks import settings
from flask import redirect, session


def requires_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('github_user_data'):
            url = settings.absurl('login')
            return redirect(url)

        return f(*args, **kwargs)

    return decorated_function
