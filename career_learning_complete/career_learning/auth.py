"""
auth.py — Login, Register, Logout
"""

import sqlite3
from flask import (Blueprint, render_template, request,
                   redirect, url_for, session, flash)
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db

auth = Blueprint('auth', __name__)


# ── Login ─────────────────────────────────────────────────────────────────────
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE username=?", (username,)
        ).fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id']  = user['id']
            session['username'] = user['username']
            session['fullname'] = user['fullname']
            session['is_admin'] = bool(user['is_admin'])
            if user['is_admin']:
                return redirect(url_for('admin.admin_panel'))
            return redirect(url_for('main.dashboard'))

        flash('Invalid username or password.', 'error')

    return render_template('login.html')


# ── Register ──────────────────────────────────────────────────────────────────
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        firstname = request.form.get('firstname', '').strip()
        lastname  = request.form.get('lastname', '').strip()
        fullname  = f"{firstname} {lastname}".strip()
        email     = request.form.get('email', '').strip().lower()
        username  = request.form.get('username', '').strip()
        s_class   = request.form.get('student_class', '')
        password  = request.form.get('password', '')
        confirm   = request.form.get('confirm_password', '')

        if not all([firstname, email, username, password]):
            flash('All fields are required.', 'error')
            return render_template('register.html')
        if password != confirm:
            flash('Passwords do not match.', 'error')
            return render_template('register.html')
        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'error')
            return render_template('register.html')

        conn = get_db()
        try:
            conn.execute(
                "INSERT INTO users (fullname,username,email,password,student_class) VALUES (?,?,?,?,?)",
                (fullname, username, email, generate_password_hash(password), s_class)
            )
            conn.commit()
            flash('Account created! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        except sqlite3.IntegrityError as e:
            if 'username' in str(e):
                flash('Username already taken. Choose another.', 'error')
            else:
                flash('Email already registered.', 'error')
        finally:
            conn.close()

    return render_template('register.html')


# ── Logout ────────────────────────────────────────────────────────────────────
@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))
