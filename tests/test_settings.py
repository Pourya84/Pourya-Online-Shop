from commerce.settings import *

SECRET_KEY = "test-secret-key"
DEBUG = False
ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
MEDIA_ROOT = "/tmp/test-media/"