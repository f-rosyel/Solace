# Solace — Django Photo Album Management System

Solace is a modern and elegant **Photo Album Management System** built with **Django**.  
It allows users to create albums, upload and manage photos, and organize memories in a clean and responsive gallery interface.

---

# ✨ Features

- 🔐 User Authentication (Login / Logout)
- 📁 Create and Manage Photo Albums
- 🖼 Upload Photos with Image Preview
- 🎨 Modern Responsive UI Design
- 📱 Mobile-Friendly Layout
- ⚡ Fast and Lightweight Django Backend
- 🗂 Organized Media and Static File Handling
- 🌙 Clean Gallery Experience

---

# 🛠 Tech Stack

| Technology | Purpose |
|---|---|
| Django | Backend Framework |
| HTML5 | Structure |
| CSS3 | Styling |
| SQLite | Database |
| Bootstrap / Custom CSS | UI Design |
| Python | Core Programming Language |

---

# 📂 Project Structure

```bash
photo_album_management_system/
│
├── albums/
├── media/
├── static/
│   └── css/
│       └── style.css
├── templates/
├── manage.py
├── db.sqlite3
└── requirements.txt
```

---

# 🚀 Installation Guide

## 1 Clone the Repository

```bash
git clone https://github.com/f-rosyel/Solace.git
cd Solace
```

---

## 2️ Create a Virtual Environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```
---

## 3️ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️ Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 5️ Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

---

## 6️ Start the Development Server

```bash
python manage.py runserver
```

Open your browser and go to:

```bash
http://127.0.0.1:8000/
```

---

# 🖼 Media Configuration

Make sure your `settings.py` contains:

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

And inside `urls.py`:

```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

# 🔒 Authentication

The system includes:
- User registration
- Secure login/logout
- Session handling
- Protected routes

---

# 📸 Future Improvements

- Like & Favorite Photos
- Comment System
- Cloud Storage Integration
- AI Photo Tagging
- Dark Mode
- Social Sharing

---

# 🧑‍💻 Author

GitHub:  
https://github.com/f-rosyel

---
