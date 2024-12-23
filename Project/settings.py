"""
Django settings for Project project.

Generated by 'django-admin startproject' using Django 4.2.16.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path
import django_heroku
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-%96)6ff&jul#v-8$mf0@z1wers+0sfmwq9#z!opa58nb(p*&vy"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True

ALLOWED_HOSTS = ['b-24-project-a4519c79ccd0.herokuapp.com/','localhost','127.0.0.1']


# Application definition
# 1 for heroku, 3 for local test!
SITE_ID = 1

INSTALLED_APPS = [
    'enroll',
    'notice_board',
    'storages',
    'dashboard',
    'crispy_forms',
    'crispy_bootstrap4',
    'login',
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
]

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": [
            "profile",
            "email"
        ],
        "AUTH_PARAMS": {"access_type": "online", "prompt": "select_account"}
    }
}

SOCIALACCOUNT_LOGIN_ON_GET=True

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "Project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, 'templates')],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "Project.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "EST"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
# os.path.join(BASE_DIR, 'static'),
]
django_heroku.settings(locals())

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend"
]

LOGIN_REDIRECT_URL = "login_page"
LOGOUT_REDIRECT_URL = "login_page"

CRISPY_TEMPLATE_PACK = 'bootstrap4'


AWS_STORAGE_BUCKET_NAME = 'pma-bucket1'
AWS_S3_FILE_OVERWRITE = False
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME


# Specifies the storage backend for static files
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'

# Specifies the storage backend for user-uploaded media files
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


'''

ACCOUNT_USERNAME_REQUIRED = False  # Disable the username requirement
ACCOUNT_SIGNUP_FORM_CLASS = None  # Skip custom signup forms
ACCOUNT_AUTHENTICATION_METHOD = "email"  # Authenticate using email
ACCOUNT_EMAIL_REQUIRED = True  # Ensure email is required
ACCOUNT_UNIQUE_EMAIL = True  # Ensure unique emails across users
SOCIALACCOUNT_AUTO_SIGNUP = True  # Allow automatic signup
ACCOUNT_SIGNUP_REDIRECT_URL = "normal_user_page"

SOCIALACCOUNT_ADAPTER = "login.adapters.MySocialAccountAdapter"
'''