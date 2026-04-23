"""
database.py — DB connection aur initialization
"""

import sqlite3
import os
from werkzeug.security import generate_password_hash

DB_PATH = 'career.db'


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def populate_sample_tests_if_empty():
    """Auto-populate sample tests if database is empty"""
    conn = get_db()
    c = conn.cursor()
    
    # Check if tests already exist
    test_count = c.execute("SELECT COUNT(*) FROM mock_tests").fetchone()[0]
    conn.close()
    if test_count > 0:
        if test_count <= 5:
            print("📚 Detected a small sample test dataset; adding the full mock test library...")
            from populate_mock_tests import populate_sample_tests as populate_full_tests
            populate_full_tests()
        return
    
    print("📚 Populating full mock test library...")
    
    from populate_mock_tests import populate_sample_tests as populate_full_tests
    populate_full_tests()
    

def init_db():
    conn = get_db()
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id            INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname      TEXT    NOT NULL,
        username      TEXT    UNIQUE NOT NULL,
        email         TEXT    UNIQUE NOT NULL,
        password      TEXT    NOT NULL,
        student_class TEXT,
        is_admin      INTEGER DEFAULT 0,
        is_mentor     INTEGER DEFAULT 0,
        created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS results (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id     INTEGER,
        result_type TEXT,
        prediction  TEXT,
        confidence  INTEGER,
        input_data  TEXT,
        created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS mock_tests (
        id                  INTEGER PRIMARY KEY AUTOINCREMENT,
        title               TEXT NOT NULL,
        description         TEXT,
        subject             TEXT NOT NULL,
        exam_type           TEXT,
        total_questions     INTEGER NOT NULL,
        duration            INTEGER,
        difficulty_level    TEXT DEFAULT 'Medium',
        created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS questions (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        mock_test_id    INTEGER NOT NULL,
        question_text   TEXT NOT NULL,
        question_type   TEXT DEFAULT 'MCQ',
        marks           INTEGER DEFAULT 1,
        image_url       TEXT,
        question_order  INTEGER,
        created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(mock_test_id) REFERENCES mock_tests(id) ON DELETE CASCADE
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS options (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        question_id     INTEGER NOT NULL,
        option_text     TEXT NOT NULL,
        option_order    INTEGER,
        is_correct      INTEGER DEFAULT 0,
        created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(question_id) REFERENCES questions(id) ON DELETE CASCADE
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS test_attempts (
        id                  INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id             INTEGER NOT NULL,
        mock_test_id        INTEGER NOT NULL,
        score               INTEGER,
        total_questions     INTEGER,
        percentage          REAL,
        answers_json        TEXT,
        attempted_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY(mock_test_id) REFERENCES mock_tests(id) ON DELETE CASCADE
    )''')

    # Default admin 
    if not c.execute("SELECT id FROM users WHERE username='admin'").fetchone():
        c.execute(
            "INSERT INTO users (fullname,username,email,password,is_admin) VALUES (?,?,?,?,?)",
            ('Administrator', 'admin', 'admin@career.learning',
             generate_password_hash('admin123'), 1)
        )
        print("✅ Admin created  →  username: admin  |  password: admin123")

    conn.commit()
    conn.close()

    # Phone column 
    try:
        conn = get_db()
        conn.execute("ALTER TABLE users ADD COLUMN phone TEXT")
        conn.commit()
        conn.close()
    except sqlite3.OperationalError:
        pass
    
    # Auto-populate sample tests if database is empty
    populate_sample_tests_if_empty()
