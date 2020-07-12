from helitrack.settings.common import *
import dj_database_url

CORS_ORIGIN_WHITELIST = [
    'https://helitrack-angular.herokuapp.com',
    'https://helitrack-frontend.herokuapp.com',
    'http://localhost:4200',
    'http://localhost:5000',
    'http://10.0.0.102:3000',
    'https://helitrack-svelte.herokuapp.com',
]

DATABASES = {
    'default': dj_database_url.config(conn_max_age=0, ssl_require=True)
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'oniizdevautsya@gmail.com'
EMAIL_HOST_PASSWORD = 'neofgoqiwhonqwam'
EMAIL_USE_SSL = True

FRONTEND_URL = CORS_ORIGIN_WHITELIST[0]
