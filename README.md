# BlogPost Full-Stack Application

This is a **full-stack web application** built with **React** for the frontend and **Django** for the backend. It is a simple blogging platform where users can register, login, create, edit, and view blog posts.

* **Frontend:** React handles all user interfaces, routing, and state management. The frontend is built as a Single Page Application (SPA) using **React Router** for navigation and can be served by Django in production.
* **Backend:** Django REST Framework (DRF) provides API endpoints for all CRUD operations on posts and user management.
* **Authentication:** Custom JWT-based authentication is implemented to secure API endpoints. Users register with email/phone and password, which is hashed before storing in the database. Upon successful login, a JWT token is issued with a 1-hour expiration.

---

## Project Structure

```
project-root/
├─ backend/               # Django backend
│  ├─ blogpost/           # Django project folder
│  │  ├─ settings.py
│  │  ├─ urls.py
│  │  └─ wsgi.py
│  ├─ manage.py
│  └─ requirements.txt
├─ frontend/blogpostui/   # React frontend
│  ├─ package.json
│  ├─ src/
│  │  ├─ App.jsx
│  │  └─ pages/
│  │      ├─ Home.jsx
│  │      ├─ Dashboard.jsx
│  │      └─ PostDetails.jsx
│  └─ public/
│      └─ index.html
└─ README.md
```

---

## Prerequisites

* Python 3.11
* Node.js & npm
* PostgreSQL or SQLite (or your preferred database)

---

## Installation & Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd project-root
```

### 2. Backend Setup (Django)

```bash
cd backend
# Create a virtual environment
python -m venv venv
source venv/bin/activate       # Linux/macOS
venv\Scripts\activate          # Windows

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Create a superuser (optional for admin access)
python manage.py createsuperuser

# Start Django server
python manage.py runserver
```

* Django runs on `http://localhost:8000/` by default
* API endpoints available under `/api/`
* JWT authentication is required for secured endpoints

---

### 3. Frontend Setup (React)

```bash
cd ../frontend/blogpostui
# Install dependencies
npm install

# Start development server
npm start
```

* React runs on `http://localhost:3000/` by default
* React development server supports hot-reloading
* All frontend requests to `/api/...` should be proxied to Django backend (can configure `proxy` in `package.json`)

---

### 4. Build React for Production

```bash
npm run build
```

* React build files will be generated in `frontend/blogpostui/build/`

---

## Features

* User registration and login with custom JWT authentication
* Create, read, update, and delete blog posts
* React SPA with routing for Home, Dashboard, and Post Details pages
* Django REST Framework provides secure API endpoints
* Passwords are hashed before storing in the database
* JWT tokens expire after 1 hour for security

---

## Notes

* React routing is handled by React Router. Django serves `index.html` for all frontend routes.
* API endpoints and frontend routes are separate, allowing SPA behavior without page reloads.
