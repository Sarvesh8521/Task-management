# ✅ TaskFlow — Task Management System

A production-grade, Jira-style team task tracker with role-based access control. 
Features a complete backend API built with Django & DRF, and a sleek, premium dark-mode Single Page Application (SPA) frontend built with Vanilla JavaScript, HTML, and CSS.

---

## 🧠 What It Does

TaskFlow allows teams to seamlessly create, assign, and monitor tasks with a full lifecycle workflow.
- **Admins** manage organizations, projects, and users.
- **Members** track their work, update task statuses, and collaborate.
- **Everything** is handled through a clean REST API and a responsive, dynamic web interface.

---

## 🛠️ Tech Stack

### Backend
- **Python + Django** — Core backend framework
- **Django REST Framework (DRF)** — REST API layer
- **PostgreSQL** — Relational database
- **JWT (SimpleJWT)** — Secure, stateless authentication

### Frontend
- **Vanilla JavaScript (ES6+)** — Client-side logic, routing, and state management without heavy frameworks
- **HTML5 & CSS3** — Semantic structure with a custom-built, variable-driven CSS design system
- **Architecture** — Single Page Application (SPA) served directly by Django

---

## ✨ Key Features

- 🎨 **Premium UI/UX:** A stunning dark-mode interface with micro-animations, toast notifications, and interactive modals.
- 📋 **Kanban Board:** Full drag-and-drop kanban board to visually manage tasks across statuses (To Do → In Progress → In Review → Completed → Blocked).
- 📊 **Dashboard:** Real-time statistics, priority breakdowns, and status charts.
- 👥 **Role-based Access:** Superusers and sub-users with distinct permissions across organizations and projects.
- 🏷️ **Rich Task Metadata:** Priority tagging, issue types (Epic, Story, Task, Bug), sprint tracking, and user assignments.
- 🔐 **Secure Authentication:** JWT-based login with automatic token refresh handling.

---

## 🚀 How to Run Locally

Because the frontend is integrated directly into the Django static files system, you **do not** need a separate Node.js server to run the frontend. Running the Django server runs the entire stack!

### Option 1: Using Python Virtual Environment (Recommended for Development)

1. **Clone the repo**
   ```bash
   git clone https://github.com/Sarvesh8521/Task-management.git
   cd Task-management
   ```

2. **Set up PostgreSQL Database**
   Ensure PostgreSQL is running on your machine. Create a database and user matching the credentials in the `.env` file (or update the `.env` file to match your local Postgres setup). By default, it expects:
   - Database Name: `task_management_db`
   - User: `task_user`
   - Password: `8521`

3. **Create and activate a virtual environment**
   ```bash
   python -m venv .venv
   
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

6. **Run the server**
   ```bash
   python manage.py runserver
   ```

7. **Access the Application**
   Open your browser and navigate to: **[http://localhost:8000/](http://localhost:8000/)**
   - The frontend is served directly by Django!
   - Click **"Sign Up"** on the login page to securely register your first user account through the API.

### Option 2: Using Docker (Recommended for Production/Testing)

1. **Ensure Docker Desktop is running.**
2. **Build and start the containers:**
   ```bash
   docker-compose up --build
   ```
3. **Access the app** at `http://localhost:8000/`. The database migrations are applied automatically by the Docker startup script.

---

## 📌 Core API Endpoints

All endpoints are prefixed with `/api/`.

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/login/` | User login (Returns JWT & User data) |
| POST | `/api/auth/token/refresh/` | Refresh JWT access token |
| GET | `/api/tasks/all/` | List all tasks |
| POST | `/api/tasks/create/` | Create a task |
| PUT | `/api/tasks/update/<id>/` | Update task fields/status |
| DELETE | `/api/tasks/delete/<id>/` | Soft-delete a task |
| GET | `/api/projects/all/` | List all projects |
| POST | `/api/organizations/create/`| Create an organization |

*(Many more endpoints exist for Users, Profiles, Projects, and Organizations. Check `task_management/urls.py` for the full routing table).*

---

## 👨‍💻 Author

**Sarvesh Singh** — [Portfolio](https://sarvesh-resume.vercel.app/) • [LinkedIn](https://www.linkedin.com/in/hire-sarvesh/)
