from django.test import TestCase
from django.conf import settings
settings.configure(
            DATABASE_ENGINE = 'djongo',
            DATABASE_NAME = 'cluster0',
            DATABASE_USER = 'dbadmi',
            DATABASE_PASSWORD = 'dbpass',
            DATABASE_HOST = 'cluster0.2agwj.mongodb.net',
            TIMEZONE = 'UTC'
)










from crypto_app.models import Crypto

# Create your tests here.
