"""
prediction.py — ML Models (Random Forest) + Predict Routes
"""

import numpy as np
import json
from flask import Blueprint, request, jsonify, session
from sklearn.ensemble import RandomForestClassifier
from database import get_db
from decorators import login_required

prediction = Blueprint('prediction', __name__)


# ════════════════════════════════════════════════════════════════════════════
#  ML MODELS
# ════════════════════════════════════════════════════════════════════════════

class StreamPredictor:
    """Class 10 → Science / Commerce / Arts"""
    STREAMS   = ['Science', 'Commerce', 'Arts']
    INTERESTS = {'technical': 0, 'business': 1, 'creative': 2}

    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=200, max_depth=8,
            min_samples_split=4, random_state=42
        )
        self._train()

    def _generate_data(self, n=800):
        rng = np.random.default_rng(42)
        X, y = [], []
        for _ in range(n):
            math    = int(rng.integers(30, 101))
            science = int(rng.integers(30, 101))
            sst     = int(rng.integers(30, 101))
            english = int(rng.integers(30, 101))
            quiz    = int(rng.integers(0, 4))
            intr    = int(rng.integers(0, 3))

            sci = math*0.35 + science*0.30 + quiz*8 + (25 if intr==0 else 6)
            com = math*0.20 + english*0.15 + sst*0.10 + quiz*6 + (30 if intr==1 else 8)
            art = english*0.25 + sst*0.25 + quiz*4 + (30 if intr==2 else 5)

            mx = max(sci, com, art)
            label = 0 if mx == sci else (1 if mx == com else 2)

            X.append([math, science, sst, english, quiz, intr])
            y.append(label)
        return np.array(X), np.array(y)

    def _train(self):
        X, y = self._generate_data()
        self.model.fit(X, y)
        print(f"✅ StreamPredictor trained  (samples={len(y)})")

    def predict(self, math, science, sst, english, quiz_score, interest):
        intr = self.INTERESTS.get(interest, 0)
        X = np.array([[math, science, sst, english, quiz_score, intr]])
        pred_idx   = self.model.predict(X)[0]
        proba      = self.model.predict_proba(X)[0]
        confidence = int(round(proba[pred_idx] * 100))
        return self.STREAMS[pred_idx], confidence, {
            s: int(round(proba[i]*100)) for i, s in enumerate(self.STREAMS)
        }


class CareerPredictor:
    """Class 12 → Engineering / Medical / Finance / Civil Services"""
    CAREERS = ['Engineering', 'Medical', 'Finance/Management', 'Civil Services']
    STREAMS = {'pcm': 0, 'pcb': 1, 'commerce': 2, 'arts': 3}
    GOALS   = {'engineering': 0, 'medical': 1, 'finance': 2, 'civil_services': 3}

    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=200, max_depth=8,
            min_samples_split=4, random_state=42
        )
        self._train()

    def _generate_data(self, n=800):
        rng = np.random.default_rng(99)
        X, y = [], []
        for _ in range(n):
            stream = int(rng.integers(0, 4))
            c1     = int(rng.integers(30, 101))
            c2     = int(rng.integers(30, 101))
            c3     = int(rng.integers(30, 101))
            quiz   = int(rng.integers(0, 4))
            goal   = int(rng.integers(0, 4))
            avg    = (c1+c2+c3)/3

            aff = {0: [35,3,10,5], 1: [5,38,4,3], 2: [3,2,38,10], 3: [2,3,10,38]}
            scores = list(aff[stream])
            marks_boost = avg / 100 * 25
            for i in range(4):
                scores[i] += marks_boost
            scores[0] += quiz * 5
            scores[3] += quiz * 6
            scores[goal] += 22

            label = int(np.argmax(scores))
            X.append([stream, c1, c2, c3, quiz, goal])
            y.append(label)
        return np.array(X), np.array(y)

    def _train(self):
        X, y = self._generate_data()
        self.model.fit(X, y)
        print(f"✅ CareerPredictor trained  (samples={len(y)})")

    def predict(self, stream, core1, core2, core3, quiz_score, goal):
        s = self.STREAMS.get(stream, 0)
        g = self.GOALS.get(goal, 0)
        X = np.array([[s, core1, core2, core3, quiz_score, g]])
        pred_idx   = self.model.predict(X)[0]
        proba      = self.model.predict_proba(X)[0]
        confidence = int(round(proba[pred_idx] * 100))
        return self.CAREERS[pred_idx], confidence, {
            c: int(round(proba[i]*100)) for i, c in enumerate(self.CAREERS)
        }


# ── Models train karo startup pe ─────────────────────────────────────────────
print("🤖 Training ML models…")
stream_model  = StreamPredictor()
career_model  = CareerPredictor()
print("🚀 ML models ready!\n")


# ════════════════════════════════════════════════════════════════════════════
#  ROUTES
# ════════════════════════════════════════════════════════════════════════════

@prediction.route('/predict/10th', methods=['POST'])
@login_required
def predict_10th():
    d = request.get_json()
    pred, confidence, scores = stream_model.predict(
        math=int(d.get('math', 75)),
        science=int(d.get('science', 75)),
        sst=int(d.get('sst', 75)),
        english=int(d.get('english', 75)),
        quiz_score=int(d.get('quiz_score', 1)),
        interest=d.get('interest', 'technical')
    )
    return jsonify({'prediction': pred, 'confidence': confidence,
                    'scores': scores, 'model': 'Random Forest Classifier'})


@prediction.route('/predict/12th', methods=['POST'])
@login_required
def predict_12th():
    d = request.get_json()
    pred, confidence, scores = career_model.predict(
        stream=d.get('stream', 'pcm'),
        core1=int(d.get('core1', 75)),
        core2=int(d.get('core2', 75)),
        core3=int(d.get('core3', 75)),
        quiz_score=int(d.get('quiz_score', 1)),
        goal=d.get('goal', 'engineering')
    )
    return jsonify({'prediction': pred, 'confidence': confidence,
                    'scores': scores, 'model': 'Random Forest Classifier'})


@prediction.route('/save-result', methods=['POST'])
@login_required
def save_result():
    d = request.get_json()
    conn = get_db()
    conn.execute(
        "INSERT INTO results (user_id, result_type, prediction, confidence, input_data) VALUES (?,?,?,?,?)",
        (session['user_id'], d.get('type'), d.get('prediction'),
         d.get('confidence', 0), json.dumps(d.get('input_data', {})))
    )
    conn.commit()
    conn.close()
    return jsonify({'status': 'saved'})
