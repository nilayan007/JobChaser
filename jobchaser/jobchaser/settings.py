"""
Django settings for jobchaser project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
from datetime import timedelta
from pathlib import Path
import os
from os import getenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-*m%*7o48#srs27-(v!b+q4pw0=+heabhvyx#$ht^x6s7tv_(kv'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'account',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'phone_field',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'corsheaders.middleware.CorsMiddleware', #cors
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'jobchaser.urls'

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

WSGI_APPLICATION = 'jobchaser.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

#DATABASES = {
#    "default": {
#        "ENGINE": "django.db.backends.mysql",
#         "NAME": "jobchaser",
#         "USER": "root",
#         "PASSWORD": "nilayan123",
#         "HOST": "127.0.0.1",
#         "PORT": "3306",
#     }
# }
#cockroach db
# DATABASES = {
#     'default': {
#         'ENGINE': 'django_cockroachdb',
#         'NAME': 'Jobchaserdb',
#         'USER': 'JobChaser',
#         'PASSWORD': 'xBnO7kWereuJQJ_7E7X13g',
#         'HOST': 'localhost',
#         'PORT': '26257',
#         # If connecting with SSL, include the section below, replacing the
#         # file paths as appropriate.
#         'OPTIONS': {
#             'sslmode': 'verify-full',
#             'sslrootcert': '/certs/ca.crt',
#             # Either sslcert and sslkey (below) or PASSWORD (above) is
#             # required.
#             'sslcert': '/certs/client.myprojectuser.crt',
#             'sslkey': '/certs/client.myprojectuser.key',
#             # If applicable
#             'options': '--cluster={routing-id}',
#         },
#     },
# }
DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME':'jobchaserdb',
    'USER': 'jobchaserdb_owner',
    'PASSWORD': 'kXWCwTIFs50N',
    'HOST': 'ep-lively-dream-a189jj0d.ap-southeast-1.aws.neon.tech',
    #'PORT': getenv('PGPORT', 5432),
    'PORT': '5432', 
    'OPTIONS': {
      'sslmode': 'require',
    },
  }
}
REST_FRAMEWORK = {
   
    'DEFAULT_AUTHENTICATION_CLASSES': (
        
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ]
   
   
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'account.User' # using custom usermodel
#email configuration

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('EMAIL_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASS')
EMAIL_USE_TLS = True

SIMPLE_JWT = {
    
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),

    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM": "jti",

    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}

PASSWORD_RESET_TIMEOUT = 900 # 900 sec = 15min 
CORS_ALLOWED_ORIGINS = ['*']


ALLOWED_HOSTS = ['*']
