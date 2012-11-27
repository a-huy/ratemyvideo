import os

PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
SETTINGS_PATH = os.path.abspath(os.path.dirname(__file__))
GEOIP_PATH = os.path.join(PROJECT_PATH, 'geoip/')
if SETTINGS_PATH != '/home/andy/code/heroku/ratemyvideo/ratemyvideo':
    DOMAIN = 'http://www.ratemyvideo.co/'
else: DOMAIN = 'http://localhost:8000/'

DEBUG = True
if SETTINGS_PATH != '/home/andy/code/heroku/ratemyvideo/ratemyvideo': DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Andy', 'anguyenhuy@gmail.com'),
    ('Server', 'ratemyvideos@gmail.com')
)

ADMIN_MEDIA_PREFIX = '/admin-media/'

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'ratemyvideo',                      # Or path to database file if using sqlite3.
        'USER': 'andy',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_PATH, 'content/assets/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/content/assets/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'tz9tv-kb2pu=a8kbcxpf+vrvjzs9ieh6r!*c=d7*yl!%*gl5sp'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = {
    'django.core.context_processors.media',
    'django.core.context_processors.csrf',
    'django.contrib.auth.context_processors.auth',
}

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'ratemyvideo.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'ratemyvideo.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, 'templates'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'base',
    'accounts',
    'videos',
    'homepage',
    'rmvadmin',
    'south',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# Email settings
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ['SENDGRID_USERNAME']
EMAIL_HOST_PASSWORD = os.environ['SENDGRID_PASSWORD']
SERVER_EMAIL = 'ratemyvideos@gmail.com'

# Configure Django to use Heroku's Postgres db
if SETTINGS_PATH != '/home/andy/code/heroku/ratemyvideo/ratemyvideo':
    import dj_database_url
    DATABASES['default'] = dj_database_url.config()

# Login Redirect
LOGIN_URL = '/rmvadmin/login'

# Facebook App Info
if SETTINGS_PATH != '/home/andy/code/heroku/ratemyvideo/ratemyvideo':
    FACEBOOK_APP_ID = '397851696951181'
    FACEBOOK_APP_SECRET = 'c4edd2b230320164c5aee64c3a10bb4d'
else:
    FACEBOOK_APP_ID = '327510684023594'
    FACEBOOK_APP_SECRET = 'e5f2b10d26a977dd9b7805152dcf2a8c'
FACEBOOK_SCOPE = 'email,user_birthday,user_location,read_stream'

# CONSTANTS
URL_MAX_LENGTH = 2048
FB_ID_MAX_LENGTH = 100
REAL_NAME_MAX_LENGTH = 200
YT_ID_MAX_LENGTH = 11
YT_TITLE_MAX_LENGTH = 2048
QUESTION_MAX_LENGTH = 2048
LOCATION_MAX_LENGTH = 300
EMAIL_MAX_LENGTH = 254
GENDER_MAX_LENGTH = 10
DESC_MAX_LENGTH = 2048
KEY_MAX_LENGTH = 128

