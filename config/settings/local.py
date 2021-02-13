"""Django settings for local development of the mysite project."""

from .base import *

env.read_env(str(ROOT_DIR / ".envs/local.env"))

SECRET_KEY = env("SECRET_KEY")

DEBUG = env("DEBUG")


# Database settings
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ROOT_DIR / "db.sqlite3",
    }
}
# Development - disable automatic static file handling
INSTALLED_APPS = ["whitenoise.runserver_nostatic"] + INSTALLED_APPS

# Emails will go to console
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Debug logging
LOGGING = {
    "version": 1,
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
        }
    },
    "loggers": {
        "django.db.backends": {
            "level": "DEBUG",
            "handlers": ["console"],
        }
    },
}
