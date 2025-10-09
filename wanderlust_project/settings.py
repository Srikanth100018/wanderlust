import os
import sys
from pathlib import Path
from decouple import config, Csv
import dj_database_url

# -------------------- BASE --------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------- ENVIRONMENT --------------------
ENV = config("ENV", default="development")  # "development" or "production"

# -------------------- SECURITY --------------------
SECRET_KEY = config("SECRET", default="django-insecure-key")
DEBUG = config("DEBUG", default=(ENV == "development"), cast=bool)

ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    default="127.0.0.1,localhost",
    cast=Csv()
)

# -------------------- INSTALLED APPS --------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",

    # Third-party apps
    "rest_framework",
    "rest_framework.authtoken",
    "widget_tweaks",
    "corsheaders",

    # Local apps
    "users",
    "listings",
    "bookings",
    "payments",
]

# -------------------- MIDDLEWARE --------------------
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "wanderlust_project.urls"

# -------------------- TEMPLATES --------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "wanderlust_project.wsgi.application"

# -------------------- DATABASE --------------------
DATABASES = {
    "default": dj_database_url.config(
        default=config("DATABASE_URL", default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}"),
        conn_max_age=600,
        ssl_require=(ENV == "production")  # SSL only in production
    )
}

# -------------------- AUTH --------------------
AUTH_USER_MODEL = "users.User"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 10,
}

# -------------------- I18N --------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# -------------------- STATIC & MEDIA --------------------
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"] if (BASE_DIR / "static").exists() else []
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# -------------------- RAZORPAY (optional) --------------------
RAZORPAY_KEY_ID = config("RAZORPAY_KEY_ID", default=None)
RAZORPAY_KEY_SECRET = config("RAZORPAY_KEY_SECRET", default=None)
RAZORPAY_WEBHOOK_SECRET = config("RAZORPAY_WEBHOOK_SECRET", default=None)

# -------------------- CLOUDINARY --------------------
CLOUD_NAME = config("CLOUD_NAME", default="")
CLOUD_API_KEY = config("CLOUD_API_KEY", default="")
CLOUD_API_SECRET = config("CLOUD_API_SECRET", default="")

# -------------------- CORS --------------------
CORS_ALLOW_ALL_ORIGINS = ENV == "development"  # Allow all only in dev
CORS_ALLOW_CREDENTIALS = True

# -------------------- SECURITY --------------------
CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

if ENV == "production":
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# -------------------- LOGGING --------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler", "stream": sys.stdout}},
    "root": {"handlers": ["console"], "level": "ERROR"},
}
