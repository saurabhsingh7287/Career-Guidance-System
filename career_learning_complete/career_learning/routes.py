"""
routes.py — General Routes (Dashboard, Profile, Resources, etc.)
"""

from datetime import datetime
from flask import Blueprint, render_template, session
from database import get_db
from decorators import login_required

main = Blueprint('main', __name__)


# ── Public ────────────────────────────────────────────────────────────────────
@main.route('/')
def index():
    return render_template('user_interface.html')


# ── Protected ─────────────────────────────────────────────────────────────────
@main.route('/dashboard')
@login_required
def dashboard():
    conn = get_db()
    user = conn.execute("SELECT is_mentor FROM users WHERE id = ?", (session['user_id'],)).fetchone()
    conn.close()
    return render_template('front.html', 
                         fullname=session.get('fullname', 'Student'),
                         is_mentor=user['is_mentor'] if user else False)


@main.route('/10th')
@login_required
def tenth():
    return render_template('10th.html')


@main.route('/12th')
@login_required
def twelfth():
    return render_template('12th.html')


@main.route('/result')
@login_required
def result():
    return render_template('result.html')


@main.route('/profile')
@login_required
def profile():
    conn = get_db()
    user = conn.execute(
        "SELECT fullname, email, phone FROM users WHERE id=?",
        (session['user_id'],)
    ).fetchone()
    results_raw = conn.execute(
        "SELECT result_type as type, prediction, confidence, created_at "
        "FROM results WHERE user_id=? ORDER BY created_at DESC",
        (session['user_id'],)
    ).fetchall()
    conn.close()

    results = []
    for r in results_raw:
        r = dict(r)
        if isinstance(r.get('created_at'), str):
            try:    r['created_at'] = datetime.strptime(r['created_at'], '%Y-%m-%d %H:%M:%S')
            except: r['created_at'] = None
        results.append(type('Result', (), r)())

    return render_template('profile.html',
        fullname=user['fullname'] if user else '',
        email=user['email'] if user else '',
        phone=user['phone'] if user else '',
        results=results
    )


@main.route('/resource')
@login_required
def resource():
    return render_template('resource.html')


@main.route('/collage')
@login_required
def collage():
    return render_template('collage.html')


@main.route('/exam-tracker')
@login_required
def exam_tracker():
    return render_template('exam_tracker.html')


@main.route('/cutoff')
@login_required
def cutoff():
    return render_template('cutoff_predictor.html')
