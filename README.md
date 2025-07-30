# Quiz-Master---V2
“Modern App Dev II Project - Quiz Platform with Flask, Vue, Redis, Celery”


# 🧠 Quiz Master

A full-stack web application that allows users to take quizzes, track their scores, and receive email reports. Admins can manage subjects, chapters, quizzes, and questions with full CRUD functionality.

---


## 🛠️ Tech Stack

| Frontend              | Backend          | Database | Auth         | Others                       |
|-----------------------|------------------|----------|--------------|------------------------------|
| Vue 3 (Options API)   | Flask (Python)   | SQLite   | JWT (Flask-JWT-Extended) | Celery, Redis, Flask-Mail    |
| Chart.js              | Flask-Restful    | SQLAlchemy ORM |           | Bootstrap 5, Fetch API      |

---

## ✨ Features

### 👥 User Side:
- Login and take quizzes
- Timer-based quiz interface
- View quiz history and performance summary
- Interactive pie and bar charts of quiz performance
- Download quiz summary via email as CSV
- View personal profile

### 🛠️ Admin Side:
- Add/edit/delete Subjects, Chapters, Quizzes, and Questions
- View dashboard summary with charts (attempts per subject, top scorers)
- Secure admin-only routes with JWT
- Manage quiz structure easily

### 📧 Email Integration:
- Users can request a CSV report of their quiz history
- Monthly email summary report using Celery + Redis + Flask-Mail
- Reminder emails for unattempted quizzes

---


## 🧪 Project Structure (Partial)

```
Quiz_Master_Project/
│
├── eraf_backend/
│   ├── eraf_api.py
│   ├── eraf_models.py
│   ├── eraf_task.py
│   ├── eraf_utils.py
│   └── __init__.py
│
├── app.py             # Main Flask App
├── celeryconfig.py    # Celery Setup
├── requirements.txt
│
├── eraf_frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Eraf_Login.vue
│   │   │   ├── Eraf_AdminSummary.vue
│   │   │   ├── Eraf_UserSummary.vue
│   │   │   └── Eraf_UserProfile.vue
│   │   └── App.vue
│   └── package.json
```

---

## 📦 Setup Instructions

### 🔧 Backend (Flask)

```bash
cd eraf_backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

### ⚙️ Start Redis & Celery

```bash
# Start Redis
redis-server

# In another terminal, start Celery worker
celery -A app.celery worker --loglevel=info

# Start Celery beat scheduler
celery -A app.celery beat --loglevel=info
```

### 🌐 Frontend (Vue 3)

```bash
cd eraf_frontend
npm install
npm run dev
```

---

## 🔐 Authentication

- JWT-based auth for users and admins
- Role-based route guards
- Secure admin dashboard

---

## 📩 Email Tasks with Celery

- Celery + Redis for background email sending
- Scheduled monthly quiz summaries
- On-demand CSV summary emails

---

## 📁 Export to CSV (Email)
```bash
GET /export_details
Header: Authorization: Bearer <user_token>
```

> The server will email the user a CSV summary of quiz attempts.

---

## 🙋‍♂️ Author

**Eraf Ali**  
IITM BS Program - Modern Application Development II  
GitHub: [https://github.com/23f2003509/Quiz-Master---V2]

---


