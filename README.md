# Personal Expense Management Backend with JWT Authentication

**Author**: [Yousef M. Y. AlSabbah](https://github.com/Yosef-AlSabbah)  
**Student ID**: 120212265  
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

---

## Project Overview

The Personal Expense Management Backend is a robust API solution designed using the Django REST Framework (DRF). This project provides users with seamless management of their financial records, including expenses, incomes, and reports. With state-of-the-art security, scalability, and performance optimizations, this backend is suitable for personal financial tracking.

---

## Features

- **Authentication**: Utilizes JSON Web Tokens (JWT) with short-lived (15 minutes) access tokens and long-lived (7 days) refresh tokens.
- **Email Verification**: Includes email-based account activation and password reset functionality.
- **Secure Endpoints**: Implements strong validation and exception handling techniques.
- **Simple History**: Tracks changes to models for audit purposes.
- **API Documentation**: Auto-generated API documentation using `drf-spectacular`.
- **Expense and Income Tracking**: Allows for categorization, update, and reporting of financial records.
- **PostgreSQL Integration**: Uses PostgreSQL for database management.
- **Scalable Architecture**: Well-structured codebase for scalability and maintainability.
- **Asynchronous Tasks**: Supports scheduled tasks using Celery and Django Celery Beat.

---

## Technologies Used

- **Framework**: Django 5.1.3
- **Database**: PostgreSQL
- **Authentication**: Djoser + JWT
- **Task Queue**: Celery + Django Celery Beat
- **API Standards**: DRF + drf-spectacular
- **Testing**: Pytest
- **Version Control**: Django Simple History
- **Security**: CORS Headers + Environment Configuration

---

## Installation and Setup

### Prerequisites
1. Install [Python](https://www.python.org/) (version >= 3.8).
2. Install PostgreSQL.

### Installation Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/Yosef-AlSabbah/Personal-Expense-Management-Application.git
   cd Personal-Expense-Management-Application
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows, use `env\Scripts\activate`
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure the `.env` file with the following variables:
   ```env
   DB_NAME=PEMA
   DB_USER=django_client
   DB_PASSWORD=0
   DB_HOST=localhost
   DB_PORT=5432
   ```

5. Run migrations to set up the database:
   ```bash
   python manage.py migrate
   ```

6. Start the development server:
   ```bash
   python manage.py runserver
   ```

### Testing
- **Custom Settings**: Use the provided settings file for running tests.
- Run the test suite:
   ```bash
   pytest
   ```

---

## Environment Variables

This project relies on a `.env` file for sensitive configurations. Below are the required variables:

- `DB_NAME` - PostgreSQL database name
- `DB_USER` - Database user
- `DB_PASSWORD` - Database password
- `DB_HOST` - Database host (default: localhost)
- `DB_PORT` - Database port (default: 5432)

---

## Endpoints Documentation

### User Management

| HTTP Method | Endpoint                 | Description                       |
|-------------|--------------------------|-----------------------------------|
| `GET`       | `/api/v1/auth/me/`       | Retrieve user profile            |
| `PUT`       | `/api/v1/auth/me/`       | Update user profile              |
| `PATCH`     | `/api/v1/auth/me/`       | Partially update user profile    |
| `DELETE`    | `/api/v1/auth/me/`       | Delete user account              |

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

1. **Exception Handling**: The project implements comprehensive exception handling techniques to ensure reliability.
2. **Validation Techniques**: Strong validation is in place for inputs, ensuring data integrity and preventing vulnerabilities.
3. **High Security**: JWT authentication and secure database configurations enhance security.
4. **API Standards**: All responses follow a consistent and standardized format for better client integration.
5. **Documentation**: Includes `drf-spectacular` for easily navigating the API endpoints.

---

## License
This project is for educational purposes under the guidance of Instructor: Mohammed El-Agha and is not intended for commercial use.
