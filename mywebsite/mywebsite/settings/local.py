from .base import *

DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": PSQL_NAME,
        "USER": PSQL_USER,
        "PASSWORD": PSQL_PASSWORD,
        "HOST": PSQL_HOST,
        "PORT": PSQL_PORT,
    }
}
