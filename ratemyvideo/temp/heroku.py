import os
import dj_database_url

DOMAIN = 'http://www.ratemyvideo.co/'
DEBUG = False
TEMPLATE_DEBUG = DEBUG

os.environ['MEMCACHE_SERVERS'] = os.environ['MEMCACHIER_SERVERS']
os.environ['MEMCACHE_USERNAME'] = os.environ['MEMCACHIER_USERNAME']
os.environ['MEMCACHE_PASSWORD'] = os.environ['MEMCACHIER_PASSWORD']
CACHES = {
    'default': {
        'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
        'LOCATION': os.environ['MEMCACHIER_SERVERS'],
        'TIMEOUT': 500,
        'BINARY': True,
    }
}

DATABASES = {
    'default': dj_database_url.config()
}

# Sendgrid credentials
EMAIL_HOST_USER = os.environ['SENDGRID_USERNAME']
EMAIL_HOST_PASSWORD = os.environ['SENDGRID_PASSWORD']

# Facebook app info
FACEBOOK_APP_ID = '397851696951181'
FACEBOOK_APP_SECRET = 'c4edd2b230320164c5aee64c3a10bb4d'