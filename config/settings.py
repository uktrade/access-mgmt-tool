# -*- coding: utf-8 -*-
from pathlib import Path

import dj_database_url
import environ
import sentry_sdk

import sys

# from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration

# Build paths inside the project like this: BASE_DIR / "subdir".
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, False),
    RESTRICT_ADMIN=(bool, False),
)

ENV_FILE = Path.joinpath(BASE_DIR, ".env")

if ENV_FILE.exists():
    environ.Env.read_env(ENV_FILE)

VCAP_SERVICES = env.json("VCAP_SERVICES", {})


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don"t run with debug turned on in production!
DEBUG = env.bool("DEBUG")
DEBUG_LEVEL = env("DEBUG_LEVEL", default="INFO")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

# Deployment environment
DEPLOYMENT_ENVIRONMENT = env("DEPLOYMENT_ENVIRONMENT", default="dev")

# GITHUB variables
GITHUB_API_URL = env("GITHUB_API_URL", default="https://api.github.com/")
GITHUB_AUTH_TOKEN = env("GITHUB_AUTH_TOKEN")
GITHUB_ORG_NAME = env("GITHUB_ORG_NAME")

LOGGING = {
    "version": 1.0,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "stream": sys.stdout,
        },
    },
    "loggers": {
        "root": {
            "handlers": ["console"],
            "level": f"{DEBUG_LEVEL}",
        },
    },
}

# Test Specific settings
if (
    DEPLOYMENT_ENVIRONMENT.lower() != "prod"
    or DEPLOYMENT_ENVIRONMENT.lower() != "production"
):
    TEST_GIT_ACCOUNT = env("TEST_GIT_ACCOUNT")
    TEST_GIT_TEAMS = env.list("TEST_GIT_TEAMS")

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework.authtoken",
    "authbroker_client",
    "application",
    "core",
    "api",
    "request",
    "github",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

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

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {"default": dj_database_url.config()}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# sentry_sdk.init(
#     env("SENTRY_DSN"),
#     environment=env("SENTRY_ENVIRONMENT"),
#     integrations=[
#         DjangoIntegration(),
#         # CeleryIntegration()
#     ]
# )

AUTHBROKER_URL = env("AUTHBROKER_URL")
AUTHBROKER_CLIENT_ID = env("AUTHBROKER_CLIENT_ID")
AUTHBROKER_CLIENT_SECRET = env("AUTHBROKER_CLIENT_SECRET")
AUTHBROKER_STAFF_SSO_SCOPE = "read write"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "authbroker_client.backends.AuthbrokerBackend",
]

LOGIN_REDIRECT_URL = "admin:index"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PARSER_CLASSES": ("rest_framework.parsers.JSONParser",),
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}
