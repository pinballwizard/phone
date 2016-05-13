"""
Django settings for phone project.

Generated by 'django-admin startproject' using Django 1.8.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'y832d7w)zo6w=xu2!w*2#fuq-l$lhn6pmr9sqx))9e+zn4k02k'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'phonebook',
    'sms',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'phone.urls'

ADMINS = (
    ('LinuxAdmin', 'linux@kraseco24.ru'),
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'phone.wsgi.application'

# AUTHENTICATION_BACKENDS = (
#     'django_auth_ldap.backend.LDAPBackend',
#     'django.contrib.auth.backends.ModelBackend',
# )
#
# AUTH_LDAP_SERVER_URI = "ldap://dc0.ksk.loc"

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'phone',
        'USER': 'django',
        'PASSWORD': 'G2x?bhlo',
        'HOST': 'orchis.ksk.loc',
        'PORT': '3306',
        'default-character-set': 'utf8',
        'collate': 'utf8_general_ci',
    },
    'asterisk': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'asterisk',
        'USER': 'asterisk',
        'PASSWORD': 'G2x?bhlo',
        'HOST': 'orchis.ksk.loc',
        'PORT': '3306',
        'default-character-set': 'utf8',
        'collate': 'utf8_general_ci',
    },
    # 'sms_info': {
    #     'NAME': 'DataForSMS',
    #     'ENGINE': 'sqlserver_pymssql',
    #     'HOST': 'ksql02.ksk.loc',
    #     'USER': 'rd',
    #     'PASSWORD': 'L151?t%fr',
    # }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Asia/Krasnoyarsk'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = 'media/'

#Email settings
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'mail.kraseco24.ru'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'sccm@kraseco24.ru'
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True
# EMAIL_USE_SSL = True