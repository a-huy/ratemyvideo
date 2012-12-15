import os

PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
SETTINGS_PATH = os.path.abspath(os.path.dirname(__file__))
GEOIP_PATH = os.path.join(PROJECT_PATH, 'geoip/')
MEDIA_ROOT = os.path.join(PROJECT_PATH, 'content/assets/')
MEDIA_URL = '/content/assets/'

ADMINS = (
    ('Dev', 'dev@ratemyvideo.co'),
)

ADMIN_MEDIA_PREFIX = '/admin-media/'

MANAGERS = (
    ('Jessica', 'jessica@ratemyvideo.co'),
    ('Andy', 'andy@ratemyvideo.co')
)

# Django default setting variables
TIME_ZONE = 'America/Los_Angeles'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_ROOT = ''
STATIC_URL = '/static/'
STATICFILES_DIRS = ()
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)
SECRET_KEY = 'tz9tv-kb2pu=a8kbcxpf+vrvjzs9ieh6r!*c=d7*yl!%*gl5sp'
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
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
ROOT_URLCONF = 'ratemyvideo.urls'
WSGI_APPLICATION = 'ratemyvideo.wsgi.application'
TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, 'templates'),
)
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    # 'django.contrib.admindocs',
    'base',
    'accounts',
    'videos',
    'homepage',
    'rmvadmin',
    'south',
)
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
SERVER_EMAIL = 'ratemyvideos@gmail.com'

LOGIN_URL = '/rmvadmin/login'

# Facebook app info
FACEBOOK_SCOPE = 'email,user_birthday,user_location,read_stream'