# ✅ Task Management System

A Jira-style team task tracker with role-based access control — built with Django & DRF.

---

## 🧠 What It Does

Teams can create, assign, and monitor tasks with a full lifecycle workflow.
Admins manage members; members track their work — all through a clean REST API.

---

## 🛠️ Tech Stack

- **Python + Django** — backend framework
- **Django REST Framework (DRF)** — REST API layer
- **PostgreSQL** — database
- **JWT** — authentication

---

## 🚀 How to Run
```bash
# 1. Clone the repo
git clone https://github.com/Sarvesh8521/Task-management.git
cd Task-management

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup database
python manage.py migrate

# 5. Run server
python manage.py runserver
```

---

## ✨ Key Features

- 👥 Role-based access — Admin vs Member permissions
- 📋 Full task lifecycle: To-Do → In Progress → Done
- 🏷️ Priority tagging and user assignment
- 🔐 JWT authentication

---

## 📌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/login/` | User login |
| GET | `/api/tasks/` | List all tasks |
| POST | `/api/tasks/` | Create a task |
| PATCH | `/api/tasks/<id>/` | Update task status |
| DELETE | `/api/tasks/<id>/` | Delete a task |

---

## 👨‍💻 Author

**Sarvesh Singh** — [Portfolio](https://sarvesh-resume.vercel.app/) • [LinkedIn](https://www.linkedin.com/in/hire-sarvesh/)
