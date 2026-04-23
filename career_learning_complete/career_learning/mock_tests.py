"""
mock_tests.py — Mock Test Module (Create, Attempt, Results)
"""

import json
from datetime import datetime
from flask import Blueprint, request, jsonify, session, render_template
from database import get_db
from decorators import login_required

mock_tests = Blueprint('mock_tests', __name__)


# ════════════════════════════════════════════════════════════════════════════
#  ROUTES
# ════════════════════════════════════════════════════════════════════════════

@mock_tests.route('/mocktest')
@login_required
def mocktest_dashboard():
    """Main Mock Test Dashboard"""
    conn = get_db()
    tests = conn.execute(
        """SELECT id, title, subject, exam_type, total_questions, duration, 
                  difficulty_level, created_at 
           FROM mock_tests 
           ORDER BY created_at DESC"""
    ).fetchall()
    conn.close()
    return render_template('mocktest.html', tests=tests)


@mock_tests.route('/api/mocktest/list')
@login_required
def get_mock_tests():
    """Get all available mock tests"""
    conn = get_db()
    tests = conn.execute(
        """SELECT id, title, subject, exam_type, total_questions, duration, 
                  difficulty_level, created_at 
           FROM mock_tests 
           ORDER BY created_at DESC"""
    ).fetchall()
    conn.close()
    
    return jsonify([dict(t) for t in tests])


@mock_tests.route('/api/mocktest/submit', methods=['POST'])
@login_required
def submit_test():
    """Submit test answers and calculate score"""
    data = request.json
    test_id = data.get('test_id')
    answers = data.get('answers', {})  # {question_id: option_id}
    
    user_id = session['user_id']
    conn = get_db()
    
    # Get test info
    test = conn.execute(
        "SELECT total_questions FROM mock_tests WHERE id = ?",
        (test_id,)
    ).fetchone()
    
    if not test:
        conn.close()
        return jsonify({'error': 'Test not found'}), 404
    
    # Calculate score
    correct = 0
    total = 0
    detailed_answers = []
    
    for question_id_str, selected_option_id_str in answers.items():
        question_id = int(question_id_str)
        selected_option_id = int(selected_option_id_str) if selected_option_id_str else None
        
        # Get correct option
        correct_option = conn.execute(
            """SELECT id FROM options 
               WHERE question_id = ? AND is_correct = 1""",
            (question_id,)
        ).fetchone()
        
        is_correct = (selected_option_id == correct_option['id']) if correct_option else False
        if is_correct:
            correct += 1
        total += 1
        
        detailed_answers.append({
            'question_id': question_id,
            'selected_option_id': selected_option_id,
            'correct_option_id': correct_option['id'] if correct_option else None,
            'is_correct': is_correct
        })
    
    # Calculate percentage
    percentage = (correct / total * 100) if total > 0 else 0
    
    # Store attempt in database
    attempt_id = conn.execute(
        """INSERT INTO test_attempts (user_id, mock_test_id, score, total_questions, 
                                      percentage, answers_json, attempted_at)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (user_id, test_id, correct, total, percentage, 
         json.dumps(detailed_answers), datetime.now().isoformat())
    ).lastrowid
    conn.commit()
    conn.close()
    
    return jsonify({
        'attempt_id': attempt_id,
        'score': correct,
        'total': total,
        'percentage': round(percentage, 2),
        'correct_answers': correct,
        'detailed_answers': detailed_answers
    })


@mock_tests.route('/api/mocktest/history')
@login_required
def get_test_history():
    """Get user's test attempt history"""
    user_id = session['user_id']
    conn = get_db()
    
    history = conn.execute(
        """SELECT ta.id, ta.mock_test_id, mt.title, mt.subject, 
                  ta.score, ta.total_questions, ta.percentage, ta.attempted_at
           FROM test_attempts ta
           JOIN mock_tests mt ON ta.mock_test_id = mt.id
           WHERE ta.user_id = ?
           ORDER BY ta.attempted_at DESC""",
        (user_id,)
    ).fetchall()
    conn.close()
    
    return jsonify([dict(h) for h in history])


@mock_tests.route('/api/mocktest/result/<int:attempt_id>')
@login_required
def get_test_result(attempt_id):
    """Get detailed result of a test attempt"""
    user_id = session['user_id']
    conn = get_db()
    
    attempt = conn.execute(
        """SELECT id, mock_test_id, score, total_questions, percentage, 
                  answers_json, attempted_at
           FROM test_attempts 
           WHERE id = ? AND user_id = ?""",
        (attempt_id, user_id)
    ).fetchone()
    
    if not attempt:
        conn.close()
        return jsonify({'error': 'Result not found'}), 404
    
    test = conn.execute(
        "SELECT title, subject, duration FROM mock_tests WHERE id = ?",
        (attempt['mock_test_id'],)
    ).fetchone()
    
    detailed_answers = json.loads(attempt['answers_json'])
    
    # Get question details for review
    questions_review = []
    for answer_detail in detailed_answers:
        question = conn.execute(
            "SELECT question_text, question_type, marks FROM questions WHERE id = ?",
            (answer_detail['question_id'],)
        ).fetchone()
        
        selected_option = conn.execute(
            "SELECT option_text FROM options WHERE id = ?",
            (answer_detail['selected_option_id'],)
        ).fetchone()
        
        correct_option = conn.execute(
            "SELECT option_text FROM options WHERE id = ?",
            (answer_detail['correct_option_id'],)
        ).fetchone()
        
        questions_review.append({
            'question_id': answer_detail['question_id'],
            'question_text': question['question_text'],
            'selected_option': selected_option['option_text'] if selected_option else 'Not Answered',
            'correct_option': correct_option['option_text'] if correct_option else None,
            'is_correct': answer_detail['is_correct'],
            'marks': question['marks']
        })
    
    conn.close()
    
    return jsonify({
        'test': dict(test),
        'attempt': {
            'id': attempt['id'],
            'score': attempt['score'],
            'total': attempt['total_questions'],
            'percentage': attempt['percentage'],
            'attempted_at': attempt['attempted_at']
        },
        'questions_review': questions_review
    })


@mock_tests.route('/api/mocktest/<int:test_id>')
@login_required
def get_test_questions(test_id):
    """Get all questions for a specific test"""
    conn = get_db()
    
    test = conn.execute(
        "SELECT id, title, subject, total_questions, duration FROM mock_tests WHERE id = ?",
        (test_id,)
    ).fetchone()
    
    if not test:
        conn.close()
        return jsonify({'error': 'Test not found'}), 404
    
    questions = conn.execute(
        """SELECT id, question_text, question_type, marks, image_url 
           FROM questions WHERE mock_test_id = ? 
           ORDER BY question_order ASC""",
        (test_id,)
    ).fetchall()
    
    questions_list = []
    for q in questions:
        q_dict = dict(q)
        options = conn.execute(
            """SELECT id, option_text, is_correct 
               FROM options WHERE question_id = ? 
               ORDER BY option_order ASC""",
            (q['id'],)
        ).fetchall()
        q_dict['options'] = [{'id': o['id'], 'text': o['option_text']} for o in options]
        questions_list.append(q_dict)
    
    conn.close()
    
    return jsonify({
        'test': dict(test),
        'questions': questions_list
    })


@mock_tests.route('/api/admin/mocktest/create', methods=['POST'])
@login_required
def create_mock_test():
    """Admin: Create a new mock test"""
    user_id = session.get('user_id')
    conn = get_db()
    
    # Check if admin
    user = conn.execute("SELECT is_admin FROM users WHERE id = ?", (user_id,)).fetchone()
    if not user or not user['is_admin']:
        conn.close()
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    test_id = conn.execute(
        """INSERT INTO mock_tests (title, description, subject, exam_type, 
                                   total_questions, duration, difficulty_level)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (data['title'], data.get('description', ''), data['subject'], 
         data['exam_type'], data['total_questions'], data['duration'], 
         data.get('difficulty_level', 'Medium'))
    ).lastrowid
    conn.commit()
    conn.close()
    
    return jsonify({'test_id': test_id, 'message': 'Test created successfully'})


@mock_tests.route('/api/admin/mocktest/<int:test_id>/add-question', methods=['POST'])
@login_required
def add_question(test_id):
    """Admin: Add a question to mock test"""
    user_id = session.get('user_id')
    conn = get_db()
    
    # Check if admin
    user = conn.execute("SELECT is_admin FROM users WHERE id = ?", (user_id,)).fetchone()
    if not user or not user['is_admin']:
        conn.close()
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    question_id = conn.execute(
        """INSERT INTO questions (mock_test_id, question_text, question_type, 
                                  marks, image_url, question_order)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (test_id, data['question_text'], data.get('question_type', 'MCQ'), 
         data.get('marks', 1), data.get('image_url'), data.get('question_order', 0))
    ).lastrowid
    
    # Add options
    for idx, option_text in enumerate(data.get('options', [])):
        is_correct = 1 if (idx == data.get('correct_option_index', 0)) else 0
        conn.execute(
            """INSERT INTO options (question_id, option_text, option_order, is_correct)
               VALUES (?, ?, ?, ?)""",
            (question_id, option_text, idx, is_correct)
        )
    
    conn.commit()
    conn.close()
    
    return jsonify({'question_id': question_id, 'message': 'Question added'})
