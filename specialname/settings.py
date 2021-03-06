"""
Django settings for specialname project.

Generated by 'django-admin startproject' using Django 1.9.6.

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
SECRET_KEY = 'syi@7f*#acr%o9a=a--_&m*#f1!90om827e!jo8zpj(cf#81i#'

IS_PRODUCTION_ENV = 'SERVER_SOFTWARE' in os.environ

if IS_PRODUCTION_ENV:
    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True
    HOSTNAME = 'www.namechinesename.com' #'http://54.69.158.70'
    # live
    PAYPAL_CLIENT_ID = 'AUm5R0abEKULUvSusff8MhrEvhyKHtnHW3oo5N0KzhjS52Ep1lVyvY4rfXLbYTYO334n6RZl2mSNo7jo'
    PAYPAL_CLIENT_SECRET = 'EHf3EVvSUO9UmBRSNtBntf4D5JsP-3swtpc0U9BzlZEUeERtVcWqGHJN_wBMGfZhMzFGJQdL2bCCXOe_'
else:
    DEBUG = True
    HOSTNAME = 'http://localhost:8000'
    # sandbox
    PAYPAL_CLIENT_ID = 'AaaPugJL3aRgMCXPBsyF8kB0CWTp4KIv8qHHIrT0RCyfC9sFOdU475Dhp-O_Qrz1cVm_afuMEnlvcYTf'
    PAYPAL_CLIENT_SECRET = 'ECKE9pvmGa_IGKUQz35vt4a_Lsv71y0OxBRLRgvQsSQJR7c0V9UP2Bu80nz_hVlo0mDhIlKk8fj8hAi-'



ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'specialname',
]

MIDDLEWARE_CLASSES = [
    # 'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'specialname.urls'

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

WSGI_APPLICATION = 'specialname.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
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

STATIC_ROOT = 'static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

