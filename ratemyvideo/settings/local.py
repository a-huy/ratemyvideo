import os

DOMAIN = 'http://localhost:5000'
DEBUG = True
TEMPLATE_DEBUG = DEBUG

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'ratemyvideo',                      # Or path to database file if using sqlite3.
        'USER': 'andy',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': 'localhost',             # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

STATIC_URL = '/content/static/'

# Sendgrid credentials
EMAIL_HOST_USER = 'app8527592@heroku.com'
EMAIL_HOST_PASSWORD = '9ywnpddt'

# Facebook app info
FACEBOOK_APP_ID = '327510684023594'
FACEBOOK_APP_SECRET = 'e5f2b10d26a977dd9b7805152dcf2a8c'

if os.path.abspath(os.path.dirname(__file__)) == '/home/andy/code/heroku/ratemyvideo/ratemyvideo/settings':
    pass
