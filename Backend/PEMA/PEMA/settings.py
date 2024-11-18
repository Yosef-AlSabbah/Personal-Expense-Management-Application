"""
Django settings for PEMA project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
from datetime import timedelta
from os import environ
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = environ.get('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = environ.get('DEBUG') == '1'

ALLOWED_HOSTS = []

# Django default apps
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# Third-party apps
THIRD_PARTY_APPS = [
    'rest_framework',  # Django REST framework
    'rest_framework.authtoken',  # Token authentication for DRF
    'djoser',  # Authentication-related endpoints
    'rest_framework_simplejwt',  # Jason Web Token for authentication
    'rest_framework_simplejwt.token_blacklist',
    'drf_spectacular',  # Spectacular for API documentation
    'corsheaders',  # Cross-Origin Resource Sharing headers
    'simple_history',  # Historical tracking for models
    'django_celery_beat',  # Periodic task scheduler with Celery
]

# Custom project apps
CUSTOM_APPS = [
    'users',  # Custom user app for managing authentication and profiles
    'expenses',  # App for expense tracking
    'income',  # App for managing income records
    'reports',  # App for generating reports
]

# Combine all app lists into INSTALLED_APPS
INSTALLED_APPS = DJANGO_APPS + CUSTOM_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'PEMA.urls'

#      ╭──────────────────────────────────────────────────────────╮
#      │                  Django Rest Framework                   │
#      ╰──────────────────────────────────────────────────────────╯
# ━━━━━━━━━━━━━━━━ THIS SECTION CONFIGURES THE REST FRAMEWORK SETTINGS. ━━━━━━━━━━━━━━━━

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        # Global permission to require authentication for all views
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FormParser',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

#      ╭──────────────────────────────────────────────────────────╮
#      │                   Email Configuration                    │
#      ╰──────────────────────────────────────────────────────────╯
# ━━ THIS SECTION CONFIGURES THE EMAIL BACKEND FOR SENDING EMAILS IN THE APPLICATION. ━━

from django.core.mail import send_mail
from django.conf import settings

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = environ.get('EMAIL_HOST_PASSWORD')

#      ╭──────────────────────────────────────────────────────────╮
#      │                  Djoser configuration                    │
#      ╰──────────────────────────────────────────────────────────╯
# ━━━━━━━━━━━━ DJOSER CONFIGURATION FOR USER AUTHENTICATION AND MANAGEMENT ━━━━━━━━━━━━━
DJOSER = {
    # 'PERMISSIONS': {
    #     'user': ['users.permissions.IsOwnerOrAdmin'],  # For access and update
    #     'user_delete': ['users.permissions.IsOwnerOrAdmin'],  # For deletion
    #     'user_update': ['users.permissions.IsOwnerOrAdmin'],  # For deletion
    #     'user_list': ['rest_framework.permissions.IsAdminUser'],  # For listing
    #     'user_detail': ['rest_framework.permissions.IsAdminUser'],  # For details
    #     'user_create': ['users.permissions.IsNotAuthenticated'],  # For details
    # },
    'HIDE_USERS': True,
    # Specifies the custom serializers
    'SERIALIZERS': {
        'user_create': 'users.api.serializers.UserProfileSerializer',  # Register user with profile
        'user_delete': 'djoser.serializers.UserDeleteSerializer',
    },
    'LOGIN_FIELD': 'email',  # Use email for login instead of username
    'SEND_ACTIVATION_EMAIL': True,  # Send activation email upon registration
    'SEND_CONFIRMATION_EMAIL': True,  # Send confirmation email for actions like password changes
    'ACTIVATION_URL': 'activate/{uid}/{token}',  # URL endpoint for account activation

    # URL endpoints for password reset and username reset confirmations
    'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/{uid}/{token}',
    'USERNAME_RESET_CONFIRM_URL': 'username/reset/confirm/{uid}/{token}',

    'PASSWORD_RESET_SHOW_EMAIL': True,  # Show email in the password reset form
    'USERNAME_CHANGED_EMAIL_CONFIRMATION': True,  # Send confirmation email if username is changed
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION': True,  # Send confirmation email if password is changed

    # Require password retype during user creation for verification
    'USER_CREATE_PASSWORD_RETYPE': True,
}

#      ╭──────────────────────────────────────────────────────────╮
#      │       Configuration for JWT Authentication Tokens        │
#      ╰──────────────────────────────────────────────────────────╯
# ━━ THIS SECTION SETS THE DURATION FOR BOTH ACCESS AND REFRESH TOKENS IN THE APPLICATION, USING THE SIMPLE_JWT SETTINGS. ━━
SIMPLE_JWT = {
    # Sets the lifespan of the access token.
    # After 15 minutes, the access token will expire, requiring the user to use the refresh token to obtain a new access token.
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),

    # Sets the lifespan of the refresh token.
    # After 7 days, the refresh token will expire, requiring the user to re-authenticate to get a new refresh token.
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),

    # Defines the class used for authentication tokens, specifying AccessToken here
    # as the type of token used by Simple JWT.
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),

    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
}

SPECTACULAR_SETTINGS = {
    "TITLE": "PEMA API Documentation",
    "DESCRIPTION": "A backend-only API solution for managing personal finances with secure JWT authentication. Users can track income, categorize expenses (e.g., transport, food), and retrieve monthly summaries and insights. This backend allows for seamless integration of secure personal finance tracking into apps, enabling informed budgeting.",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": True,  # Enables schema serving at runtime
    "SCHEMA_PATH_PREFIX": "/api/v1",  # Filter paths for the documented schema

    # Enforce strict validation and clean documentation
    "SORT_OPERATIONS": True,  # Sort operations alphabetically by path and method
    "SORT_SCHEMA_BY_TAGS": True,  # Sort schema tags alphabetically
    "ENUM_NAME_OVERRIDES": {},  # Customize enum names if needed
    "COMPONENT_SPLIT_REQUEST": False,  # Avoid splitting components for requests and responses unnecessarily

    # Ensure compatibility with DELETE methods accepting body payloads
    "ENABLE_DELETE_METHODS_WITH_BODY": True,
    # "ENABLE_DELETE_METHODS_WITH_BODY": False,

    # Tags and grouping
    "TAGS": [
        {
            "name": "User Management",
            "description": "Endpoints for managing user profiles, accounts, and related data."
        },
        {
            "name": "User Authentication",
            "description": "Endpoints for user login, logout, and authentication."
        },
        {
            "name": "Expenses",
            "description": "Endpoints for managing user expenses."
        },
        {
            "name": "Income",
            "description": "Endpoints for managing user income."
        },
        {
            "name": "Reports",
            "description": "Endpoints for generating financial reports."
        },
    ],
    # Authentication configuration
    "SECURITY": [
        {"bearerAuth": []},  # Assuming you're using Bearer/Token-based authentication
    ],

    # Default pagination
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "DEFAULT_PAGE_SIZE": 10,  # Change as per your API's use case

    # Deprecation warnings
    "APPEND_PATH_TO_TAGS": False,  # Do not append path to tags; keeps tags clean
    "SCHEMA_EXTENSIONS": [],  # Add custom schema extensions if needed
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': "JWT Authorization header using the Bearer scheme. Example: \"Authorization: Bearer {token}\"",
        }
    },
    'USE_SESSION_AUTH': False,
}

#      ╭──────────────────────────────────────────────────────────╮
#      │                CORS ORIGIN CONFIGURATION                 │
#      ╰──────────────────────────────────────────────────────────╯
CORS_ALLOW_METHODS = (
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
)

#      ╭──────────────────────────────────────────────────────────╮
#      │        DJANGO CORN JOBS SCHEDULING CONFIGURATION         │
#      ╰──────────────────────────────────────────────────────────╯
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'PEMA.wsgi.application'

#      ╭──────────────────────────────────────────────────────────╮
#      │                    DATABASES SECTION                     │
#      ╰──────────────────────────────────────────────────────────╯

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# ━━━━━━━━━━━━━━━━━━━━━━━ DEFAULT SQLITE DATABASE CONFIGURATION ━━━━━━━━━━━━━━━━━━━━━━━━

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# ━━━━━━━━━━━━━━━━━━━━━━━━━ POSTGRESQL DATABASE CONFIGURATION ━━━━━━━━━━━━━━━━━━━━━━━━━━

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': environ.get('DB_NAME'),
        'USER': environ.get('DB_USER'),
        'PASSWORD': environ.get('DB_PASSWORD'),
        'HOST': environ.get('DB_HOST'),
        'PORT': environ.get('DB_PORT'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/jwt/create/'

AUTH_USER_MODEL = 'users.UserAccount'
USERNAME_FIELD = 'email'
