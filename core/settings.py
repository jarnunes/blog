from pathlib import Path
from django.contrib.messages import constants
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-0iom3w)c-v4(6nproe=f25&d7rld!n!#=&bbvsrnhj=jx9xq3l'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
DEBUG_PROPAGATE_EXCEPTIONS = True

ALLOWED_HOSTS = ['127.0.0.1', 'blog2.jnunesc.com.br', 'blog.jnunesc.com.br', 'blog-demo.jnunesc.com.br']
CSRF_TRUSTED_ORIGINS = ['https://blog-demo.jnunesc.com.br', 'https://blog-demo.jnunesc.com.br']

# Sitemaps
SITE_ID = 1

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.postgres',
    'blog',
    'commons',
    'taggit',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

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

WSGI_APPLICATION = 'core.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    # 'default2': {
    #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #     'NAME': env('DJGDB_NAME'),
    #     'USER': env('DJGDB_USERNAME'),
    #     'PASSWORD': env('DJGDB_PASSWORD'),
    #     'HOST': env('DJGDB_HOST'),
    #     'PORT': env('DJGDB_PORT'),
    # },
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# A linha abaixo deve ser descomentada apenas quando debug=True para evitra o erro 500
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# A linha abaixo deve ser descomentada apenas quando o debug=False
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
# STATICFILES_DIRS = [BASE_DIR / 'static/']
STATIC_ROOT = 'static/'

# Media files
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = 'media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Messages
MESSAGE_TAGS = {
    constants.ERROR: 'alert-danger',
    constants.WARNING: 'alert-warning',
    constants.SUCCESS: 'alert-success',
    constants.INFO: 'alert-primary'
}

# SMTP Settings
EMAIL_HOST = env('DJGEMAIL_HOST')
EMAIL_PORT = env('DJGEMAIL_PORT')
EMAIL_HOST_USER = env('DJEMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('DJEMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True

APPLICATION_NAME = 'e-Blog'
