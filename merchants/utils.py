from functools import wraps
from flask import g, url_for, flash, request, redirect


def requires_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            flash(u'You need to be signed in for this page.')
            return redirect(url_for('.join', next=request.path))
        return f(*args, **kwargs)
    return decorated_function
