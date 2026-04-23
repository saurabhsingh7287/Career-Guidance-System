# Career.learning — Complete Project Setup

## Project Structure
```
career_learning/
├── app.py               ← Flask backend (ML + AI Chatbot + all routes)
├── requirements.txt     ← Python dependencies
├── career.db            ← Auto-created SQLite database
└── templates/
    ├── user_interface.html  ← Landing page (public)
    ├── login.html           ← Login page
    ├── register.html        ← Register page
    ├── front.html           ← Dashboard (after login)
    ├── 10th.html            ← Class 10 Stream Predictor
    ├── 12th.html            ← Class 12 Career Predictor
    ├── result.html          ← Results page (JS engine + ML verification)
    ├── resourse.html        ← Resource portal
    ├── admin.html           ← Admin panel (admin only)
    └── chatbot.html         ← AI CareerBot (NEW)
```

## Setup Steps

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Set API Key (for AI Chatbot)
```bash
# Windows
set ANTHROPIC_API_KEY=sk-ant-your-key-here

# Mac/Linux
export ANTHROPIC_API_KEY=sk-ant-your-key-here
```
Get your free API key at: https://console.anthropic.com

### 3. Run the app
```bash
python app.py
```

### 4. Open in browser
```
http://localhost:5000
```

## Default Admin Account
- **Username:** admin
- **Password:** admin123
- **Admin Panel:** http://localhost:5000/admin

## New Features Added

### Machine Learning (Random Forest Classifier)
- **Class 10:** Predicts Science / Commerce / Arts from marks + interests + quiz
- **Class 12:** Predicts Engineering / Medical / Finance / Civil Services
- Trained on 800 synthetic samples with domain-expert rules
- Shows ML verification badge on result page
- API endpoints: `/predict/10th` and `/predict/12th`

###  AI Chatbot (Anthropic Claude)
- Fully conversational career guidance bot
- Indian context: JEE, NEET, CLAT, CA, UPSC
- Multi-turn conversation with history
- Route: `/chatbot`
- API: `/api/chat` (POST)

## All Routes
| Route | Description |
|-------|-------------|
| `GET /` | Landing page |
| `GET/POST /login` | Login |
| `GET/POST /register` | Register |
| `GET /logout` | Logout |
| `GET /dashboard` | User dashboard (login required) |
| `GET /10th` | Class 10 assessment (login required) |
| `GET /12th` | Class 12 assessment (login required) |
| `GET /result` | Results page (login required) |
| `GET /resources` | Resource portal |
| `GET /chatbot` | AI Chatbot (login required) |
| `POST /predict/10th` | ML prediction API |
| `POST /predict/12th` | ML prediction API |
| `POST /save-result` | Save result to DB |
| `POST /api/chat` | AI chatbot API |
| `GET /admin` | Admin panel (admin only) |
| `POST /admin/delete-user/<id>` | Delete user |
