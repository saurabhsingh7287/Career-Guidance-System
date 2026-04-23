"""
decorators.py — Auth Decorators (login_required, admin_required)
"""

from functools import wraps
from flask import session, redirect, url_for, flash
from database import get_db


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to continue.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        conn = get_db()
        user = conn.execute(
            "SELECT is_admin FROM users WHERE id=?", (session['user_id'],)
        ).fetchone()
        conn.close()
        if not user or not user['is_admin']:
            flash('Admin access required.', 'error')
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated
