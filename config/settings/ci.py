"""Django settings for local development of the mysite project."""

from .base import *

env.read_env(str(ROOT_DIR / ".envs/ci.env"))

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
