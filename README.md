# DevLog Archival

A Django full-stack project for DevLog, a work session tracker for creators. It includes the account feature and the core feature, work session logging.

## Tech stack
- Django
- PostgreSQL
- Supabase-ready environment variables
- Django templates for frontend rendering

## Project features
- User registration with validation
- Login and logout
- Role-based dashboards for admin and member
- Profile viewing and editing
- Protected routes using Django authentication

## Core Feature: Work Session Logging

Logged-in users create projects (with optional categories) and log work sessions
with a date, duration in minutes and notes. Members see and manage only their own
records. Admins can view and manage all sessions.

- Models: Category, Project (many-to-many with Category), WorkSession (ForeignKey to User and Project)
- Pages: /tracker/sessions/, /tracker/projects/, /tracker/categories/
- Validation: duration must be at least 1 minute, the date cannot be in the future, project and category names must be unique per user

## Setup
1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a PostgreSQL database and add the connection values in a local `.env` file.
4. Run migrations:
   ```bash
   python manage.py migrate
   ```
5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```
6. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Environment variables
Use a local `.env` file based on `.env.example`.

Example:
```env
SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=devlog_archival
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
```

## GitHub repo notes
- Keep `.env` out of version control.
- Keep `venv/` and `__pycache__/` out of version control.
- Use a public repository and commit the project in stages as it develops.
