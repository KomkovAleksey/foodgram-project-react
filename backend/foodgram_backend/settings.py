"""
Django settings for foodgram project.
"""
import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


INSECURE_KEY = 'django-insecure-0eikswwglid=ukts4l2_b=676m!-q_%154%2z@&l3)n6)cp3#c'
SECRET_KEY = os.getenv('SECRET_KEY', INSECURE_KEY)

DEBUG = os.getenv('DEBUG', 'False') == 'True'

DEVELOP = os.getenv('DEVELOP', 'False') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.1').split(', ')


INSTALLED_APPS = [
    # DJANGO_APPS
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # THIRD_PARTY_APPS
    "rest_framework",
    "rest_framework.authtoken",
    "django_filters",
    "colorfield",
    "djoser",
    "debug_toolbar",

    # LOCAL_APPS
    "api.apps.ApiConfig",
    "users.apps.UsersConfig",
    "recipes.apps.RecipesConfig",
    "core.apps.CoreConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = "foodgram_backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "foodgram_backend.wsgi.application"

AUTH_USER_MODEL = 'users.CustomUser'

if not DEVELOP:
    DATABASES = {
        "default": {
            "ENGINE": os.getenv("DB_ENGINE"),
            "NAME": os.getenv("DB_NAME"),
            "USER": os.getenv("POSTGRES_USER"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
            "HOST": os.getenv("DB_HOST"),
            "PORT": os.getenv("DB_PORT")
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


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

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
}

INTERNAL_IPS = [
    "127.0.0.1",
    "localhost",
]

DJOSER = {
    "LOGIN_FIELD": 'email',
    "HIDE_USERS": False,
    "SERIALIZERS": {
        "user_create": "api.v1.serializers.CustomUserCreateSerializer",
        "user": "api.v1.serializers.CustomUserSerializer",
        "current_user": "api.v1.serializers.CustomUserSerializer",
    },
    "PERMISSIONS": {
        "user": ["djoser.permissions.CurrentUserOrAdminOrReadOnly"],
        "user_list": ["rest_framework.permissions.IsAuthenticatedOrReadOnly"],
    },
}

LANGUAGE_CODE = "ru-RU"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_TZ = True


STATIC_URL = '/backend_static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'backend_static/')

MEDIA_URL = '/backend_media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'backend_media/')

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
