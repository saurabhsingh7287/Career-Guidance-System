"""
chatbot.py — AI Chatbot (Groq API - Llama 3.3)
"""

import requests as req
from flask import Blueprint, render_template, request, jsonify
from decorators import login_required

chatbot = Blueprint('chatbot', __name__)

# ── Groq API Key ────────────────────────────────────────────────────────────
GROQ_API_KEY = ""  # ← Sirf yahan apni key paste karo

CAREER_SYSTEM_PROMPT = """You are CareerBot, an AI career guidance assistant for Career.learning —
a platform helping Indian students (Class 10 & 12) choose the right stream and career.

Your job:
- Help decide between Science, Commerce, Arts (after Class 10)
- Suggest careers based on marks, interests, aptitude
- Guide about JEE, NEET, CA, CLAT, NDA and other Indian entrance exams
- Be encouraging, friendly, like a knowledgeable Indian mentor
- Keep responses concise (max 3-4 short paragraphs), use emojis occasionally
- Always end with a follow-up question"""


# ── Chatbot Page ──────────────────────────────────────────────────────────────
@chatbot.route('/chatbot')
@login_required
def chatbot_page():
    return render_template('chatbot.html')


# ── Chat API ──────────────────────────────────────────────────────────────────
@chatbot.route('/api/chat', methods=['POST'])
@login_required
def chat():
    d = request.get_json()
    messages = d.get('messages', [])
    if not messages:
        return jsonify({'error': 'No messages provided'}), 400

    try:
        url = "https://api.groq.com/openai/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": CAREER_SYSTEM_PROMPT},
                *[{"role": m["role"], "content": m["content"]} for m in messages]
            ],
            "temperature": 0.7,
            "max_tokens": 1024
        }

        response = req.post(url, json=payload, headers=headers, timeout=15)
        data = response.json()
        print("GROQ RESPONSE:", data)

        if 'choices' in data:
            reply = data['choices'][0]['message']['content']
            return jsonify({'reply': reply})
        else:
            error_code = data.get('error', {}).get('code', '')
            error_msg = data.get('error', {}).get('message', 'Something went wrong')

            if error_code == 'rate_limit_exceeded' or '429' in str(error_code):
                return jsonify({'reply': '⚠️ Thoda busy hoon abhi! 1-2 second wait karo aur dobara try karo. 😅'}), 200
            else:
                return jsonify({'error': error_msg}), 500

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500