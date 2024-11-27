
# Personal Expense Management Backend with JWT Authentication

**Author**: [Yousef M. Y. AlSabbah](https://github.com/Yosef-AlSabbah)  
**Instructor**: [Mohammed El-Agha](https://github.com/MohammedElagha)

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Technologies Used](#technologies-used)
4. [Installation and Setup](#installation-and-setup)
5. [Environment Variables](#environment-variables)
6. [Endpoints Documentation](#endpoints-documentation)
7. [Best Practices and Highlights](#best-practices-and-highlights)
8. [License](#license)

---

## Project Overview

The **Personal Expense Management Backend** is a powerful API built with Django and the Django REST Framework (DRF). It enables users to efficiently manage their financial records, track expenses and income, and generate reports. The system ensures high security, scalability, and performance for personal financial tracking needs.

---

## Features

- **JWT Authentication**: Secure authentication using short-lived access tokens (15 minutes) and long-lived refresh tokens (7 days).
- **Email Verification**: Supports email-based account activation and password reset functionalities.
- **Secure Endpoints**: Implements robust validation and error handling techniques for security.
- **Simple History**: Tracks changes to models for audit purposes using the `django-simple-history` package.
- **API Documentation**: Auto-generated API documentation with `drf-spectacular`.
- **Expense and Income Tracking**: Categorize, update, and report on financial transactions.
- **PostgreSQL Integration**: Uses PostgreSQL for persistent data storage.
- **Scalable Architecture**: Codebase designed for scalability and maintainability.
- **Asynchronous Tasks**: Background task processing with Celery and Django Celery Beat.

---

## Technologies Used

- **Framework**: Django 5.1.3
- **Database**: PostgreSQL
- **Authentication**: Djoser + JWT
- **Task Queue**: Celery + Django Celery Beat
- **API Documentation**: DRF + drf-spectacular
- **Testing**: Pytest
- **Version Control**: django-simple-history
- **Security**: CORS Headers, Environment Configuration

---

## Installation and Setup

### Prerequisites

1. Install [Python](https://www.python.org/) (version >= 3.8).
2. Install [PostgreSQL](https://www.postgresql.org/).

### Installation Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/Yosef-AlSabbah/Personal-Expense-Management-Application.git
   cd Personal-Expense-Management-Application/Backend/PEMA
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows, use `env\Scripts\activate`
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

### Create the PostgreSQL Database

Make sure PostgreSQL is installed and running on your system. Then, create the necessary database and user with the following steps:

```bash
psql -U postgres
```

Once inside the PostgreSQL shell, run the following commands:

```sql
CREATE DATABASE PEMA;
CREATE USER django_client WITH PASSWORD '0';
ALTER ROLE django_client SET client_encoding TO 'utf8';
ALTER ROLE django_client SET default_transaction_isolation TO 'read committed';
ALTER ROLE django_client SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE PEMA TO django_client;
```

This ensures that the `django_client` user has full access to the `PEMA` database.

---

### Run the Database Initialization Command

Once the database is created and the user has been set up, initialize the system by running the following Django management command:

```bash
python manage.py init_system.py
```

### Set Up the Superuser

To access the Django admin panel as a superuser, use the following credentials when prompted:

- **Email**: `yalsabbah@students.iugaza.edu.ps`
- **Password**: `0`

This will grant you full access to the admin interface and other system functionalities.

---

### Configure the `.env` File

Create a `.env` file in the project root directory with the following content:

```env
DB_NAME=PEMA
DB_USER=django_client
DB_PASSWORD=0
DB_HOST=localhost
DB_PORT=5432
```

### Apply Migrations

Run the following command to apply the database migrations:

```bash
python manage.py migrate
```

### Start the Development Server

Start the Django development server:

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser to access the application.

---

### Testing

To run tests, use the provided test settings file and execute the following:

```bash
pytest
```

---

## Environment Variables

The project relies on a `.env` file to manage sensitive configuration values. Below are the required environment variables:

- `DB_NAME` - PostgreSQL database name
- `DB_USER` - Database user
- `DB_PASSWORD` - Database password
- `DB_HOST` - Database host (default: `localhost`)
- `DB_PORT` - Database port (default: `5432`)

---

## Endpoints Documentation

### User Management

| HTTP Method | Endpoint                 | Description                       |
|-------------|--------------------------|-----------------------------------|
| `GET`       | `/api/v1/auth/me/`        | Retrieve user profile            |
| `PUT`       | `/api/v1/auth/me/`        | Update user profile              |
| `PATCH`     | `/api/v1/auth/me/`        | Partially update user profile    |
| `DELETE`    | `/api/v1/auth/me/`        | Delete user account              |

### User Authentication

| HTTP Method | Endpoint                       | Description                          |
|-------------|--------------------------------|--------------------------------------|
| `POST`      | `/api/v1/auth/register/`       | Register a new account              |
| `POST`      | `/api/v1/auth/activate/`       | Activate account using email        |
| `POST`      | `/api/v1/auth/token/obtain/`   | Login and obtain tokens             |
| `POST`      | `/api/v1/auth/token/refresh/`  | Refresh access token                |
| `POST`      | `/api/v1/auth/token/destroy/`  | Logout and destroy tokens           |
| `POST`      | `/api/v1/auth/reset-password/` | Request password reset              |
| `POST`      | `/api/v1/auth/reset-password-confirm/` | Confirm password reset      |

### Expenses

| HTTP Method | Endpoint                  | Description           |
|-------------|---------------------------|-----------------------|
| `POST`      | `/api/v1/expenses/create/` | Create a new expense  |

### Income

| HTTP Method | Endpoint                | Description                  |
|-------------|-------------------------|------------------------------|
| `PUT`       | `/api/v1/income/update/` | Update income record         |
| `PATCH`     | `/api/v1/income/update/` | Partially update income record |

### Reports

| HTTP Method | Endpoint                                      | Description                         |
|-------------|-----------------------------------------------|-------------------------------------|
| `GET`       | `/api/v1/reports/expenses/monthly/`           | List monthly expenses              |
| `GET`       | `/api/v1/reports/expenses/monthly/by-category/` | Categorized monthly expenses     |
| `GET`       | `/api/v1/reports/monthly-statistics/`         | Monthly financial statistics        |

---

## Best Practices and Highlights

1. **Exception Handling**: Comprehensive exception handling ensures system reliability.
2. **Input Validation**: Strong input validation prevents data issues and vulnerabilities.
3. **High Security**: Secure JWT authentication and robust database configurations ensure data safety.
4. **API Consistency**: Standardized API responses for smooth client integration.
5. **Comprehensive Documentation**: The `drf-spectacular` library auto-generates API documentation for easy reference.

---

## License

This project is for educational purposes under the guidance of Instructor [Mohammed El-Agha](https://github.com/MohammedElagha) and is not intended for commercial use.
