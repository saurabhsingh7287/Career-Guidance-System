"""
admin.py — Admin Panel Routes
"""

from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash
from database import get_db
from decorators import admin_required

admin = Blueprint('admin', __name__)


# ── Admin Dashboard ───────────────────────────────────────────────────────────
@admin.route('/admin')
@admin_required
def admin_panel():
    conn = get_db()

    users_raw = conn.execute("""
        SELECT u.*, COUNT(r.id) as result_count
        FROM users u
        LEFT JOIN results r ON r.user_id = u.id
        GROUP BY u.id
        ORDER BY u.created_at DESC
    """).fetchall()

    results_raw = conn.execute("""
        SELECT r.*, u.fullname, u.username
        FROM results r
        JOIN users u ON u.id = r.user_id
        ORDER BY r.created_at DESC
        LIMIT 50
    """).fetchall()

    test_attempts_raw = conn.execute("""
        SELECT ta.*, u.fullname, u.username, mt.title as test_title
        FROM test_attempts ta
        JOIN users u ON u.id = ta.user_id
        JOIN mock_tests mt ON mt.id = ta.mock_test_id
        ORDER BY ta.attempted_at DESC
        LIMIT 50
    """).fetchall()

    total_users   = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    total_results = conn.execute("SELECT COUNT(*) FROM results").fetchone()[0]
    total_tests   = conn.execute("SELECT COUNT(*) FROM test_attempts").fetchone()[0]
    tenth_count   = conn.execute("SELECT COUNT(*) FROM results WHERE result_type='10th'").fetchone()[0]
    twelfth_count = conn.execute("SELECT COUNT(*) FROM results WHERE result_type='12th'").fetchone()[0]

    top_raw = conn.execute("""
        SELECT prediction, COUNT(*) as cnt FROM results
        GROUP BY prediction ORDER BY cnt DESC LIMIT 6
    """).fetchall()
    top_predictions = [(r['prediction'], r['cnt']) for r in top_raw]

    users = []
    for u in users_raw:
        u = dict(u)
        if isinstance(u.get('created_at'), str):
            try:    u['created_at'] = datetime.strptime(u['created_at'], '%Y-%m-%d %H:%M:%S')
            except: u['created_at'] = None
        users.append(type('User', (), u)())

    results = []
    for r in results_raw:
        r = dict(r)
        if isinstance(r.get('created_at'), str):
            try:    r['created_at'] = datetime.strptime(r['created_at'], '%Y-%m-%d %H:%M:%S')
            except: r['created_at'] = None
        results.append(type('Result', (), r)())

    test_attempts = []
    for ta in test_attempts_raw:
        ta = dict(ta)
        if isinstance(ta.get('attempted_at'), str):
            try:    ta['attempted_at'] = datetime.strptime(ta['attempted_at'], '%Y-%m-%d %H:%M:%S')
            except: ta['attempted_at'] = None
        test_attempts.append(type('TestAttempt', (), ta)())

    conn.close()
    return render_template('admin.html',
        users=users, results=results, test_attempts=test_attempts,
        total_users=total_users, total_results=total_results, total_tests=total_tests,
        tenth_count=tenth_count, twelfth_count=twelfth_count,
        top_predictions=top_predictions
    )


# ── User Delete ───────────────────────────────────────────────────────────────
@admin.route('/admin/delete-user/<int:uid>', methods=['POST'])
@admin_required
def delete_user(uid):
    conn = get_db()
    user = conn.execute("SELECT fullname, is_admin FROM users WHERE id=?", (uid,)).fetchone()
    if not user:
        flash('User not found.', 'error')
    elif user['is_admin']:
        flash('Cannot delete admin account.', 'error')
    else:
        conn.execute("DELETE FROM results WHERE user_id=?", (uid,))
        conn.execute("DELETE FROM users WHERE id=?", (uid,))
        conn.commit()
        flash(f'User "{user["fullname"]}" deleted.', 'success')
    conn.close()
    return redirect(url_for('admin.admin_panel'))
