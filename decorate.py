from functools import wraps
from flask import redirect, url_for, session, g


def login_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        user_id = session.get('user_id', None)
        if user_id != None:
            g.user_id = user_id
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return inner
