import os
from pathlib import Path

from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(override=True)

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "default")

DEBUG_TRUE_VALUES = {"true", "1", "yes"}

DEBUG = os.getenv("DJANGO_DEBUG", "False").lower() in DEBUG_TRUE_VALUES

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "*").split(",")


INSTALLED_APPS = [
    "about.apps.AboutConfig",
    "catalog.apps.CatalogConfig",
    "core.apps.CoreConfig",
    "django_cleanup.apps.CleanupConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    "django.contrib.messages",
    "homepage.apps.HomepageConfig",
    "sorl.thumbnail",
    "tinymce",
]

if DEBUG:
    INSTALLED_APPS.append("debug_toolbar")

ALLOW_REVERSE_TRUE_VALUES = {
    "true",
    "yes",
    "1",
    "y",
    "",
}
ALLOW_REVERSE = (
    os.getenv("DJANGO_ALLOW_REVERSE", "true").lower()
    in ALLOW_REVERSE_TRUE_VALUES
)

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "lyceum.middleware.ReverseRussianWordsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
]


if DEBUG:
    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")

INTERNAL_IPS = [
    "127.0.0.1",
]

ROOT_URLCONF = "lyceum.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "lyceum.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
}


AUTH_PASSWORD_VALID = "django.contrib.auth.password_validation"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": f"{AUTH_PASSWORD_VALID}.UserAttributeSimilarityValidator",
    },
    {
        "NAME": f"{AUTH_PASSWORD_VALID}.MinimumLengthValidator",
    },
    {
        "NAME": f"{AUTH_PASSWORD_VALID}.CommonPasswordValidator",
    },
    {
        "NAME": f"{AUTH_PASSWORD_VALID}.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "ru"

LANGUAGES = [
    ("en", _("English")),
    ("ru", _("Russian")),
]

LOCALE_PATHS = [BASE_DIR / "locale"]

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


STATIC_URL = "/static/"
STATICFILES_DIRS = [
    BASE_DIR / "static_dev",
]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": [
            ["Bold", "Italic"],
            ["JustifyLeft", "JustifyCenter", "JustifyRight"],
            ["RemoveFormat"],
        ],
        "height": 300,
        "width": "100%",
    },
}
