# Copyright (c) 2012 Jason McVetta.

import dj_database_url
import os
import sys
import logging
from django.conf import global_settings


def env_setting(name, default=None):
    '''
    Attempts to return the value of `name` from environment variables.  
    If `name` is not set, logs an error message and returns default.
    '''
    try:
        result = os.environ[name]
    except:
        result = default
        msg = 'Could not load setting "%s" from environment.  App may not function correctly' % name
        logging.error(msg)
    return result


TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS
AUTHENTICATION_BACKENDS = global_settings.AUTHENTICATION_BACKENDS
    
PWD = os.getenv("PWD", "/app")

DEBUG = bool(os.environ.get('DJANGO_DEBUG', False))
if DEBUG:
    logging.warn('Application is running in DEBUG mode.')
TEMPLATE_DEBUG = DEBUG


ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {'default': dj_database_url.config(default='sqlite:///' +
        os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'db.sqlite') )}


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Los_Angeles'

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
MEDIA_ROOT = os.path.join(PWD, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PWD, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '4qs&amp;1$j%s28$np0_14q4mb^e@lub6e)2fr03e%$^x^70csha$h'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'creditswarm.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'creditswarm.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PWD, "templates"),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django_bcrypt',
    'south',
    'bootstrapform',
    'dispute',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
            },
        'simple': {
            'format': '%(levelname)s %(message)s'
            },
        },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
            },
        },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'stream': sys.stdout,
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


#-------------------------------------------------------------------------------
#
# Sendgrid
#
#-------------------------------------------------------------------------------

DEFAULT_FROM_EMAIL = 'Credit Swarm <noreply@creditswarm.com>'
EMAIL_HOST_USER = os.getenv('SENDGRID_USERNAME')
EMAIL_HOST= 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_PASSWORD = os.getenv('SENDGRID_PASSWORD')

#-------------------------------------------------------------------------------
#
# django-social-auth
#
#-------------------------------------------------------------------------------

INSTALLED_APPS += (
    'social_auth', 
)

AUTHENTICATION_BACKENDS += (
    'social_auth.backends.google.GoogleOAuth2Backend',
    'social_auth.backends.facebook.FacebookBackend',
    )

GOOGLE_OAUTH2_CLIENT_ID      = os.getenv('GOOGLE_OAUTH2_CLIENT_ID')
GOOGLE_OAUTH2_CLIENT_SECRET  = os.getenv('GOOGLE_OAUTH2_CLIENT_SECRET')
FACEBOOK_APP_ID              = os.getenv('FACEBOOK_APP_ID')
FACEBOOK_API_SECRET          = os.getenv('FACEBOOK_API_SECRET')

FACEBOOK_EXTENDED_PERMISSIONS = ['email']

LOGIN_URL          = '/login-form/'
LOGIN_REDIRECT_URL = '/'
LOGIN_ERROR_URL    = '/login-error/'

#SOCIAL_AUTH_COMPLETE_URL_NAME  = 'socialauth_complete'
#SOCIAL_AUTH_ASSOCIATE_URL_NAME = 'socialauth_associate_complete'

SOCIAL_AUTH_DEFAULT_USERNAME = 'creditswarm_user'

#SOCIAL_AUTH_EXPIRATION = 'expires'


#-------------------------------------------------------------------------------
#
# User Profile
#
#-------------------------------------------------------------------------------

INSTALLED_APPS += (
    'profile', 
)

AUTH_PROFILE_MODULE = 'profile.UserProfile'


#-------------------------------------------------------------------------------
#
# django-storages
#
#-------------------------------------------------------------------------------

INSTALLED_APPS += (
    'storages', 
)

STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
#DEFAULT_FILE_STORAGE = 'storages.backends.s3.S3Storage'

AWS_ACCESS_KEY_ID = env_setting('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env_setting('AWS_SECRET_ACCESS_KEY')
# NOTE: This bucket is publicly accessible
AWS_STORAGE_BUCKET_NAME = 'creditswarm-public'
STATIC_URL = 'https://s3.amazonaws.com/creditswarm-public'


#-------------------------------------------------------------------------------
#
# django-user-accounts
#
#-------------------------------------------------------------------------------

#INSTALLED_APPS += (
#    'account',  # django-user-accounts
#    'profile',  # User profile model & views
#)
#
#AUTH_PROFILE_MODULE = 'profile.UserProfile'
#
#
#TEMPLATE_CONTEXT_PROCESSORS += (
#    "account.context_processors.account",
#)
#
#ACCOUNT_EMAIL_UNIQUE = True
#ACCOUNT_EMAIL_CONFIRMATION_REQUIRED = True
#
#LOGIN_URL          = '/account/login'
#LOGIN_REDIRECT_URL = '/'


#-------------------------------------------------------------------------------
#
# Require SSL
#
#-------------------------------------------------------------------------------

if not (DEBUG or os.getenv('SSL_DISABLE')):
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    MIDDLEWARE_CLASSES = (
        'sslify.middleware.SSLifyMiddleware',
    ) + MIDDLEWARE_CLASSES

