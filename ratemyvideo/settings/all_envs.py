import os
import sys
import djcelery
import datetime
from celery.schedules import crontab

PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
SETTINGS_PATH = os.path.abspath(os.path.dirname(__file__))
GEOIP_PATH = os.path.join(PROJECT_PATH, 'geoip/')
MEDIA_ROOT = os.path.join(PROJECT_PATH, 'content/media/')
MEDIA_URL = '/content/media/'

ADMINS = (
    ('Dev', 'dev@ratemyvideo.co'),
)

ADMIN_MEDIA_PREFIX = '/admin-media/'

MANAGERS = (
    ('Support', 'support@ratemyvideo.co'),
)

# Django default setting variables
TIME_ZONE = 'America/Los_Angeles'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_ROOT = os.path.join(PROJECT_PATH, '/static/')
STATICFILES_DIRS = (os.path.join(PROJECT_PATH, 'content/static/'),)
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
    'django.core.context_processors.static',
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
    'kombu.transport.django',
    'djcelery',
    'ratemyvideo',
    'base',
    'accounts',
    'videos',
    'homepage',
    'rmvadmin',
    'south',
    'storages',
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

# Celery
BROKER_BACKEND = 'django'
djcelery.setup_loader()

CELERYBEAT_SCHEDULE = {
    'check-user-balances': {
        'task': 'base.tasks.check_user_balances',
        'schedule': crontab(hour=16, minute=0)
    },
    'invalidate-charts': {
        'task': 'base.tasks.invalidate_charts',
        'schedule': crontab(hour=16, minute=30)
    },
    'update-queues': {
        'task': 'base.tasks.update_queues',
        'schedule': crontab(hour=8, minute=0)
    },
    'calc-all-tslr': {
        'task': 'base.tasks.calc_all_tslr',
        'schedule': datetime.timedelta(minutes=10)
    },
    'update-graph-data': {
        'task': 'base.tasks.update_graph_data',
        'schedule': datetime.timedelta(minutes=60)
    }
}
CELERY_TIMEZONE = 'UTC'

# Email settings
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
SERVER_EMAIL = 'ratemyvideos@gmail.com'

LOGIN_URL = '/rmvadmin/login'

# Facebook app info
FACEBOOK_SCOPE = 'email,user_birthday,user_location,read_stream'

# Paypal
TEST_PAYPAL_USER = 'dev_1356037078_biz_api1.ratemyvideo.co'
TEST_PAYPAL_PASS = '1356037100'
TEST_PAYPAL_SIGNATURE = 'AFcWxV21C7fd0v3bYYYRCpSSRl31AmvJjdB608f29vuqflOhtj9lYGLO'
PAYPAL_API_VERSION = '95.0'