from helitrack.settings.common import *

ALLOWED_HOSTS = [os.environ['WEBSITE_SITE_NAME'] + '.azurewebsites.net',
                 '127.0.0.1'] if 'WEBSITE_SITE_NAME' in os.environ else []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DBNAME'],
        'HOST': os.environ['DBHOST'],
        'USER': os.environ['DBUSER'],
        'PASSWORD': os.environ['DBPASS']
    }
}

CORS_ORIGIN_WHITELIST = [
    'https://helitrack-angular.azurewebsites.net',
    'https://helitrack-frontend.azurewebsites.net',
    'https://helitrack-svelte.azurewebsites.net',
]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'oniizdevautsya@gmail.com'
EMAIL_HOST_PASSWORD = 'neofgoqiwhonqwam'
EMAIL_USE_SSL = True

FRONTEND_URL = CORS_ORIGIN_WHITELIST[0]
