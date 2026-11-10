# car_reselling_project/Backend/backend/settings.py
# This REPLACES your current settings.py completely

from pathlib import Path
import os
from datetime import timedelta
from dotenv import load_dotenv


load_dotenv()  # reads the .env file you created in the Backend folder

BASE_DIR = Path(__file__).resolve().parent.parent

# ── Security ──────────────────────────────────────────────────────
SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-dev-key')
DEBUG      = os.environ.get('DEBUG', 'False') == 'True'


# ── Apps ──────────────────────────────────────────────────────────
INSTALLED_APPS = [
    'jazzmin',
    'rest_framework',
    'corsheaders',
    'django_filters',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.postgres',
    'storages',
    'myapp',
    'rest_framework_simplejwt',
    'channels',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ← NEW: serves static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'backend.wsgi.application'
ASGI_APPLICATION  = 'backend.asgi.application'

# ── Database ──────────────────────────────────────────────────────
DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.postgresql',
        'NAME':     os.environ.get('DB_NAME',     'soorathautos_2_0'),
        'USER':     os.environ.get('DB_USER',     'soorathuser'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'StrongPassword123'),
        'HOST':     os.environ.get('DB_HOST',     'localhost'),
        'PORT':     os.environ.get('DB_PORT',     '5432'),
    }
}

# ── REST Framework ────────────────────────────────────────────────
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME":  timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}

# ── CORS ──────────────────────────────────────────────────────
ALLOWED_HOSTS = ["api.soorathautos.in", "3.25.218.45"]

CORS_ALLOWED_ORIGINS = [
    "https://soorathautos.in",
    "https://www.soorathautos.in",
    "https://prod.d1c393hp1kvmq2.amplifyapp.com",
    "http://localhost:5173",
]

# ── AWS S3 (media files) ──────────────────────────────────────────
AWS_ACCESS_KEY_ID       = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY   = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_S3_BUCKET')
AWS_S3_REGION_NAME      = os.environ.get('AWS_REGION', 'ap-south-1')
AWS_S3_CUSTOM_DOMAIN    = f'{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com'

AWS_S3_FILE_OVERWRITE   = False          # don't overwrite same-name uploads
AWS_DEFAULT_ACL          = None           # use bucket-level ACL
AWS_QUERYSTRING_AUTH     = False          # clean public URLs (no ?Signature=...)

# ── Static & Media ────────────────────────────────────────────────
STATIC_URL  = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'   # where collectstatic puts files
STATICFILES_DIRS = [BASE_DIR / 'static']
STORAGES = {
    'default': {
        'BACKEND': 'storages.backends.s3boto3.S3Boto3Storage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}

# ── Password Validation ───────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ── Internationalisation ──────────────────────────────────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE     = 'Asia/Kolkata'
USE_I18N      = True
USE_TZ        = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ── Jazzmin ───────────────────────────────────────────────────────
JAZZMIN_SETTINGS = {
    'site_header':          'Soorath Autos',
    'site_brand':           'Soorath Autos',
    'welcome_title':        'Welcome to Soorath Autos',
    'search_model':         'myapp.Vehicle',
    'user_avatar':          'user__avatar',
    'show_ui_builder':      True,
    'changeform_format':    'horizontal',
    'related_modal_active': True,
    'show_collapse':        True,
    'navigation_expanded':  True,
    'navigation_collapsed': True,
    'show_sidebar':         True,
    'navigation_icon':      'fa fa-bars',
    'site_title':           'Soorath Autos',
}
JAZZMIN_UI_TWEAKS = {
    'footer_credit':              'Soorath Autos',
    'navbar_small_text':          True,
    'footer_small_text':          True,
    'body_small_text':            True,
    'brand_small_text':           True,
    'brand_colour':               False,
    'accent':                     'accent-primary',
    'navbar':                     'navbar-white navbar-light',
    'no_navbar_border':           False,
    'navbar_fixed':               False,
    'layout_boxed':               False,
    'footer_fixed':               False,
    'sidebar_fixed':              False,
    'sidebar':                    'sidebar-dark-primary',
    'sidebar_nav_small_text':     False,
    'sidebar_disable_expand':     False,
    'sidebar_nav_child_indent':   False,
    'sidebar_nav_compact_style':  False,
    'sidebar_nav_legacy_style':   False,
    'sidebar_nav_flat_style':     False,
    'theme':                      'lumen',
    'dark_mode_theme':            None,
    'button_classes': {
        'primary':   'btn-outline-primary',
        'secondary': 'btn-outline-secondary',
        'info':      'btn-info',
        'warning':   'btn-warning',
        'danger':    'btn-danger',
        'success':   'btn-success',
    },
}
DATA_UPLOAD_MAX_MEMORY_SIZE = 52428800
FILE_UPLOAD_MAX_MEMORY_SIZE = 52428800
