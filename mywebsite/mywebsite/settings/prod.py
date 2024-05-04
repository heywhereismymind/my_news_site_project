from .base import *
import os


DEBUG = False
ALLOWED_HOSTS = ["www.mywebsiteproject.com", "mywebsiteproject.com"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get("POSTGRES_DB"),
        'USER': os.environ.get("POSTGRES_USER"),
        'PASSWORD': os.environ.get("POSTGRES_PASSWORD"),
        'HOST': "db",
        'PORT': 5432,
    }
}