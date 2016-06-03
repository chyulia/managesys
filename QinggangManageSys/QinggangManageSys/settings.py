"""
Django settings for QinggangManageSys project.

Generated by 'django-admin startproject' using Django 1.9.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@o$#tz@^1q8-(nk*8d(-r-pqdbci@*x2(hemnwnvp1&kw$@ggp'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',#the core of the authentication framework
    'django.contrib.contenttypes',#allows permissions to be associated with models you create.
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'data_import',
]


MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',#manages sessions across requests.
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',# associates users with requests using sessions.
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',#logs users out of their other sessions after a password change.
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'QinggangManageSys.urls'

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

WSGI_APPLICATION = 'QinggangManageSys.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    '1default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE': 'django.db.backends.oracle',
        'NAME': 'qinggang',
        'USER': 'qinggang',
        'PASSWORD': 'qinggang',
        'HOST': '10.30.0.152',
        'PORT': '1521',
    },
    'default': {
        'ENGINE': 'django.db.backends.oracle',
        'NAME': 'maksim',
        'USER': 'changxin',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '1521',
    },
    'mes': {
        'ENGINE': 'django.db.backends.oracle',
        'NAME': 'mesdb2',#sid:mesdb2;service:mesdb
        'USER': 'BD_query',
        'PASSWORD': 'BD_query',
        'HOST': '10.30.0.17',
        'PORT': '1521',
    },
    'l2': {
        'ENGINE': 'django.db.backends.oracle',
        'NAME': 'qgil2db',
        'USER': 'BD_query',
        'PASSWORD': 'BD_query',
        'HOST': '10.20.0.22',
        'PORT': '1521',
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'


'''
自己添加
'''
#@login_required,redirect
LOGIN_URL = '/login'

ADMINS = (
    ('Maksim Cheng', 'ccxysfh1993@gmail.com'),
)


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = False
EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = '525794244@qq.com'
EMAIL_HOST_PASSWORD = 'chengcx1993Ysfh'
DEFAULT_FROM_EMAIL = '525794244@qq.com'