# 📚 Bibliosphere Backend

Bibliosphere is a library management system backend that handles book sharing, borrowing, and user scoring to manage borrowing limits. This project provides a RESTful API built with Django and Django REST Framework.

---

## 🚀 Features

- 🔐 User registration and login with JWT authentication  
- 👥 Role-based user system (Admin, User)  
- 📊 User scoring system to determine borrowing limits and durations  
- 📚 CRUD operations for books (list, search, add, update, delete)  
- 📦 Borrow and return books functionality  
- ⏱️ Automatic score updates for late returns  
- 🧪 Testing support and sample data  

---

## 🛠️ Technologies

| Backend          | Other                | Database        |
|------------------|----------------------|-----------------|
| Python 3.13      | Django 5.x           | PostgreSQL      |
| Django REST Framework | JWT Authentication | SQLite (dev)    |

---

## ⚙️ Installation

```bash
# 1. Clone the repository
git clone https://github.com/OmerGokdemir/bibliosphere_backend.git
cd bibliosphere_backend

# 2. Create and activate virtual environment
python -m venv env
source env/bin/activate  # Windows: env\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations
python manage.py migrate

# 5. Create a superuser (optional)
python manage.py createsuperuser

# 6. Start the development server
python manage.py runserver
```

## 🔑 Environment Variables (.env)
```bash
SECRET_KEY=your_secret_key_here
```

## 📁 Project Structure

```bash
bibliosphere_backend/
│
├── core/                  # Main settings and URL configuration
├── user/                  # Custom User model and user management
├── book/                  # Book models and business logic
├── loan/                  # Borrowing and returning system
├── utils/                 # Utility functions
├── static/                # Static files
└── media/                 # Media files (e.g., book images)
```

## 📮 API Endpoints Examples

Method	| URL	| Description
---|---|---
POST|	/api/auth/register/	|Register a new user
POST|	/api/auth/login/	|Obtain JWT token
GET|	/api/books/	|List all books
POST|	/api/loan/borrow/	|Borrow a book
POST|	/api/loan/return/	|Return a borrowed book

## ✅ Running Tests

```bash
python manage.py test
```

## 📄 License

This project is licensed under the [MIT License](LICENSE).

## 🧑‍💻 Developer

Omer Gokdemir

📧 omer66gokdemir@gmail.com

🔗 [LinkedIn](https://www.linkedin.com/in/omer-gokdemir/)

🐙 [@OmerGokdemir](https://github.com/OmerGokdemir)

💼 [Upwork](https://www.upwork.com/freelancers/~01cf80f9e22cf120e3)

🌐 [Live Demo](https://skyiron.pythonanywhere.com/)


Bibliosphere is an open-source, scalable, and extensible backend foundation for book sharing and library systems.