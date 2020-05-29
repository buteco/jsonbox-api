from pathlib import Path

import belogging
from dj_database_url import parse as parse_db_url
from prettyconf import config

# Project Structure
BASE_DIR = Path(__file__).absolute().parents[2]
PROJECT_DIR = Path(__file__).absolute().parents[1]
FRONTEND_DIR = PROJECT_DIR / "frontend"

# Debug & Development
DEBUG = config("DEBUG", default=False, cast=config.boolean)

# Database
DATABASES = {"default": config("DATABASE_URL", cast=parse_db_url)}
DATABASES["default"].update(
    {
        "CONN_MAX_AGE": config("CONN_MAX_AGE", cast=config.eval, default="None"),
        "OPTIONS": {"charset": "utf8mb4", "init_command": "SET sql_mode='STRICT_TRANS_TABLES'"},
        "TEST": {"NAME": config("TEST_DATABASE_NAME", default=None), "CHARSET": "utf8mb4"},
    }
)

# Security & Signup/Signin
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="*", cast=config.list)
SECRET_KEY = config("SECRET_KEY")

# i18n & l10n
TIME_ZONE = "UTC"
USE_I18N = False
USE_L10N = False
USE_TZ = True
LANGUAGE_CODE = "en-us"

# Miscelaneous
_project_package = "jsonbox_api"
ROOT_URLCONF = "{}.urls".format(_project_package)
WSGI_APPLICATION = "{}.wsgi.application".format(_project_package)
LOG_REQUEST_ID_HEADER = "HTTP_X_REQUEST_ID"
GENERATE_REQUEST_ID_IF_NOT_IN_HEADER = True
REQUEST_ID_RESPONSE_HEADER = "RESPONSE_HEADER_NAME"
SECURE_SSL_REDIRECT = config("SSL_REDIRECT", default=True, cast=config.boolean)

# Media & Static
MEDIA_URL = "/media/"
STATIC_URL = "/static/"
_static_root = FRONTEND_DIR / "static"
STATIC_ROOT = config("STATIC_ROOT", default=_static_root)

# Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(FRONTEND_DIR / "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "debug": config("TEMPLATE_DEBUG", default=DEBUG, cast=config.boolean),
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
            ],
        },
    }
]

# Application
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "log_request_id.middleware.RequestIDMiddleware",
]

INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    # 3rd party libs
    "django_mysql",
    "rest_framework",
    "rest_framework.authtoken",
    "django_extensions",
    "drf_yasg",
    # local
    "apps.boxes",
    "apps.jsons",
    "apps.demo",
)

# Logging
LOGGING_CONFIG = None
belogging.load(enable_duplication_filter=True, json=True)

# Django REST Framework
REST_FRAMEWORK = {
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
    "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework.authentication.TokenAuthentication",),
    "UNAUTHENTICATED_USER": None,
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 25,
}

# Swagger
SWAGGER_SETTINGS = {
    "USE_SESSION_AUTH": False,
    "PERSIST_AUTH": True,
    "REFETCH_SCHEMA_WITH_AUTH": True,
    "REFETCH_SCHEMA_ON_LOGOUT": True,
    "DEFAULT_MODEL_DEPTH": 1,
    "DEFAULT_MODEL_RENDERING": "model",
    "SUPPORTED_SUBMIT_METHODS": ("get",),
    "SECURITY_DEFINITIONS": {"Token": {"type": "apiKey", "name": "Authorization", "in": "header"}},
}
