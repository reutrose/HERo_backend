# Blog Management System - Django REST API

## Project Overview

This project is a server-side web application built using Django and Django REST Framework. It provides a content management system for blog editors to create, edit, and delete articles, while registered users can write comments. The application follows role-based permissions and utilizes PostgreSQL as its database.

## Key Features

- **User Roles & Permissions**:
  - Guests: Can only view content.
  - Regular Users: Can view and comment on articles.
  - Editors: Can create, edit, and delete their own articles.
  - Administrators: Can manage all content and comments.
- **Authentication & Authorization**:
  - JWT-based authentication (djangorestframework-simplejwt)
  - User registration and profile editing
- **Article Management**:
  - CRUD operations for blog articles
  - Filtering by title, content, date, author, tags, and category
- **Commenting System**:
  - Users can comment on articles
  - Users can delete/edit their own comments
  - Admins can delete any comment
- **Database Seeding**:
  - Initial data includes 3 users, 3 articles, and 2 comments per article
- **API Documentation**:
  - Full API endpoint documentation included

## Tech Stack

- **Backend**: Django, Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: Simple JWT
- **Environment Management**: python-decouple
- **Security & CORS Handling**: django-cors-headers
- **Filtering**: django-filter

## Installation & Setup

### Prerequisites

- Python 3.8+
- PostgreSQL
- Virtual Environment (recommended)

### Steps to Set Up

1. Clone the repository:
   ```sh
   git clone https://github.com/reutrose/HERo_backend
   ```
2. Create a virtual environment and activate it:
   ```sh
   python -m venv venv
   ```
   Then in Mac:
   ```sh
   source venv/bin/activate
   ```
   Or in Windows:
   ```sh
   venv\Scripts\activate
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Set up environment variables:
   - Make sure to include an `.env` file in the project root with the relevant content.
   - If you do not have access to the `.env` file, create a PostgreSQL database in PG Admin, and then create an `.env` file that contains: (DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT).
   - For your information, that project contains an option for database seeding. For that, the `.env` file is necessary, and without it, the seeding isn't allowed.
5. Apply database migrations:
   ```sh
   python manage.py makemigrations
   ```
   ```sh
      python manage.py makemigrations api
   ```
   ```sh
   python manage.py migrate
   ```
6. Create Superuser:
   ```
   python manage.py createsuperuser
   ```
7. Seed the database:
   ```sh
   python manage.py seed_db
   ```
8. Start the development server:
   ```sh
   python manage.py runserver
   ```
9. Go to:
   ```sh
   http://127.0.0.1:8000/api/
   ```

## API Endpoints

### Authentication

- `POST /api/register/` - Register a new user
- `POST /api/token/` - Obtain access and refresh tokens
- `POST /api/token/refresh/` - Refresh authentication token

### Articles

- `GET /api/articles/` - Retrieve all articles
- `GET /api/articles/?search=<query>` - Search articles
- `GET /api/articles/<id>/` - Retrieve a specific article
- `POST /api/articles/` - Create a new article
- `PUT /api/articles/<id>/` - Edit an article
- `DELETE /api/articles/<id>/` - Delete an article

### Comments

- `GET /api/articles/<id>/comments/` - Retrieve comments for an article
- `POST /api/comments/` - Create a new comment
- `DELETE /api/comments/<id>/` - Delete a comment

## Requirements

```
asgiref==3.8.1
dj-database-url==2.3.0
Django==5.1.7
django-cors-headers==4.7.0
django-filter==25.1
django-rest-framework==0.1.0
django-seed==0.3.1
django-taggit==6.1.0
djangorestframework==3.15.2
djangorestframework_simplejwt==5.5.0
Faker==37.0.0
pillow==11.1.0
psycopg2==2.9.10
PyJWT==2.9.0
python-decouple==3.8
python-dotenv==1.0.1
sqlparse==0.5.3
toposort==1.10
typing_extensions==4.12.2
tzdata==2025.1
```

## Notes

- The `.env` file is excluded from the repository for security reasons.
- If the `.env` file is missing, you must create your own PostgreSQL database and configure the connection in the `.env` file.
- The frontend (React) is in a separate repository.

---

### License

This project is for educational purposes and is not intended for commercial use.

---

### Author

Developed as part of the Full-Stack Web Development course assignment.

- Email: rosenfeldreut@gmail.com
