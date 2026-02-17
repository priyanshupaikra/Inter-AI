# 🤖 Inter-AI

A full-stack AI-powered web application built with **React** (frontend) and **Django** (backend).

---

## 📌 What is This?

Inter-AI is a web application that combines a modern React frontend with a powerful Django backend. The project is set up and ready for building AI-powered features.

---

## 🛠️ Tech Stack

| Part      | Technology          |
|-----------|---------------------|
| Frontend  | React 19, Vite 7    |
| Backend   | Django 5.2 (Python) |
| Database  | SQLite (default)    |
| Styling   | CSS                 |

---

## 📁 Project Structure

```
Inter-AI/
├── backend/                # Django backend
│   ├── backend/
│   │   ├── __init__.py
│   │   ├── settings.py     # Django settings
│   │   ├── urls.py         # URL routing
│   │   ├── asgi.py         # ASGI config
│   │   └── wsgi.py         # WSGI config
│   └── manage.py           # Django CLI tool
├── frontend/               # React frontend
│   ├── src/
│   │   ├── App.jsx         # Main App component
│   │   ├── App.css         # App styles
│   │   ├── main.jsx        # Entry point
│   │   ├── index.css       # Global styles
│   │   └── assets/         # Static assets
│   ├── public/             # Public files
│   ├── index.html          # HTML template
│   ├── package.json        # Node dependencies
│   ├── vite.config.js      # Vite config
│   └── eslint.config.js    # ESLint config
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

Make sure you have these installed:

- **Python 3.10+** → [Download](https://www.python.org/downloads/)
- **Node.js 18+** → [Download](https://nodejs.org/)
- **pip** (comes with Python)
- **npm** (comes with Node.js)

---

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/priyanshupaikra/Inter-AI.git
cd Inter-AI
```

### 2️⃣ Set Up the Backend (Django)

```bash
cd backend

# Create a virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install Django
pip install django

# Run database migrations
python manage.py migrate

# Start the backend server
python manage.py runserver
```

The backend will run at: **http://127.0.0.1:8000**

### 3️⃣ Set Up the Frontend (React)

Open a **new terminal** and run:

```bash
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

The frontend will run at: **http://localhost:5173**

---

## 📜 Available Commands

### Backend (Django)

| Command                          | What it does               |
|----------------------------------|----------------------------|
| `python manage.py runserver`     | Start the backend server   |
| `python manage.py migrate`       | Apply database migrations  |
| `python manage.py createsuperuser` | Create an admin user     |

### Frontend (React)

| Command           | What it does                  |
|-------------------|-------------------------------|
| `npm run dev`     | Start development server      |
| `npm run build`   | Build for production          |
| `npm run preview` | Preview the production build  |
| `npm run lint`    | Check code for errors         |

---

## 🤝 Contributing

1. Fork this repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Commit (`git commit -m "Add your feature"`)
5. Push (`git push origin feature/your-feature`)
6. Open a Pull Request

---

## 📄 License

This project is open source. Feel free to use and modify it.

---

Made with ❤️ by [priyanshupaikra](https://github.com/priyanshupaikra)