# Personal Expense Management Backend with JWT Authentication

**Author:** Yousef M. Y. AlSabbah  
**Student ID:** 120212265  
**Instructor:** Mohammed El-Agha

A secure backend solution built with Django for personal expense management. This project provides APIs for tracking income and expenses, allowing for monthly summaries and insights. JWT (JSON Web Token) authentication ensures data security for each user.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Requirements](#requirements)
- [License](#license)

---

## Project Overview

This project provides a backend solution for personal expense management with JWT-based authentication. Users can:
- Track income and categorize expenses (transport, food, healthcare, etc.)
- Retrieve monthly summaries and analytics
- Securely manage their data with JWT authentication

## Features

- **JWT Authentication**: Secure user login and registration with JWT tokens.
- **Income & Expense Tracking**: Record monthly income and categorize expenses.
- **Monthly Summaries**: Retrieve data for income, expenses, and spending insights.
- **RESTful API**: Well-structured API endpoints for easy integration into front-end apps.

## Technologies Used

- **Backend Framework**: Django (Python)
- **Authentication**: JWT (JSON Web Tokens)
- **Database**: SQLite (default, can be configured for other databases)
- **Dependency Management**: Requirements file (`requirements.txt`)

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Step-by-Step Guide

1. **Clone the Repository**
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Create a Virtual Environment**
   ```bash
   python3 -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**
   Create a `.env` file in the project root directory with the following variables:
   ```bash
   SECRET_KEY=your_secret_key_here
   DEBUG=True
   ```

5. **Apply Migrations**
   ```bash
   python manage.py migrate
   ```

6. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```
   Access the server at `http://127.0.0.1:8000`.

---

## Usage

1. **Register a New User**
   Send a POST request to `/api/register` with user details to create a new account.

2. **Log In**
   Send a POST request to `/api/login` with credentials. A JWT token will be provided upon successful login.

3. **Access Secured Endpoints**
   Include the JWT token in the `Authorization` header as `Bearer <your_token>` to access protected endpoints.

---

## API Endpoints

### Authentication

- **POST** `/api/register/`: Register a new user
- **POST** `/api/login/`: Log in and obtain a JWT token

### Income & Expenses

- **POST** `/api/income/`: Add monthly income
- **POST** `/api/expenses/`: Add an expense with category
- **GET** `/api/summary/`: Retrieve monthly income and expense summaries

---

## Requirements

All dependencies are listed in `requirements.txt`. Install them using:

```bash
pip install -r requirements.txt
```

---

## Running Tests

To run the test suite, use:

```bash
python manage.py test
```

---

## License

This project is for educational purposes under the guidance of **Instructor: Mohammed El-Agha** and is not intended for commercial use.

---

## Notes

For animations and transitions in documentation, refer to GitHub's markdown-supported tools for rich formatting. Additionally, using external tools like **GitHub Pages** or **MkDocs** can provide a more interactive experience for documentation if hosted separately.

--- 

This README provides a comprehensive guide, including installation, API usage, and instructions for running the project, ensuring ease of setup and understanding for developers who want to work with or build upon this backend solution.
