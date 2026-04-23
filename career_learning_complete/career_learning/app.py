"""
app.py — Career.learning | Main Entry Point
"""

import os
from flask import Flask
from database import init_db

# ── App Initialize ────────────────────────────────────────────────────────────
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'career_learning_2026_secret')

# ── Blueprints Register  ──────────────────────────────────────────────────
from auth       import auth
from routes     import main
from prediction import prediction
from chatbot    import chatbot
from admin      import admin
from mock_tests import mock_tests

app.register_blueprint(auth)
app.register_blueprint(main)
app.register_blueprint(prediction)
app.register_blueprint(chatbot)
app.register_blueprint(admin)
app.register_blueprint(mock_tests)

# ── Run ───────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
