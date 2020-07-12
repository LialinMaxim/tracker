from helitrack.settings.common import *

DEBUG = True

CORS_ORIGIN_WHITELIST = [
    'http://localhost:4200',
    'http://10.0.0.102:3000',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'helitrack',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

FRONTEND_URL = 'https://helitrack-angular.herokuapp.com'
