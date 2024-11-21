from PEMA.settings import *

# Override settings specific to testing
SECRET_KEY = 'django-insecure-km0g10%jx@f+rqsxg)wgop#3ie&gqnys41^9aa!iyv&ywyjoul'
DEBUG = True
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # Avoid real email sending
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',  # Use SQLite for faster tests
#         'NAME': 'PEMA',
#         'USER': 'django_client',
#         'PASSWORD': '0',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Use SQLite for faster tests
        'NAME': ':memory:',
    }
}
