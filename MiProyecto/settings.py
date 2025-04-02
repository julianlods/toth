import os
import dj_database_url
import cloudinary
import cloudinary.uploader
import cloudinary.api
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

ENVIRONMENT = os.getenv("ENV", "production")

if ENVIRONMENT == "local":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASE_URL = os.getenv("DATABASE_URL")
    DATABASES = {
        "default": dj_database_url.parse(DATABASE_URL, conn_max_age=600, ssl_require=True)
    }

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "django-insecure-v6v33$75$5!iod698(o)k%=3%kd&7%_lom*lm$h#w*@#2(j%j@")

# Configuración dinámica de DEBUG
DEBUG = os.getenv("DEBUG", "True") == "True" if os.getenv("ENV") == "local" else False

ALLOWED_HOSTS = [
    "toth-project.onrender.com",  # Dominio correcto de Render
    "127.0.0.1",
    "localhost"
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary_storage',
    'cloudinary',
    'toth',  # Agrega tu app personalizada
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # WhiteNoise para servir archivos estáticos en producción
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'MiProyecto.urls'

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

WSGI_APPLICATION = 'MiProyecto.wsgi.application'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Argentina/Buenos_Aires'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Se necesita para producción en Render
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

STATICFILES_DIRS = [
    BASE_DIR / 'toth' / 'static',  # Ruta a la carpeta 'static' dentro de la app 'toth'
]

# Configuración de archivos subidos por usuarios
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Asegurar que Render sirva archivos media correctamente
if "RENDER" in os.environ:
    MEDIA_URL = "https://toth-project.onrender.com/media/"
else:
    MEDIA_URL = "/media/"

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuración del modelo de usuario personalizado
AUTH_USER_MODEL = 'toth.Usuario'

# Configuración de autenticación personalizada
AUTHENTICATION_BACKENDS = [
    'toth.backends.AuthBackend',  # Tu backend personalizado
    'django.contrib.auth.backends.ModelBackend',  # Backend predeterminado de Django
]

# Configuración de sesión
SESSION_COOKIE_SECURE = False  # Cambiar a True en producción con HTTPS
CSRF_COOKIE_SECURE = False     # Cambiar a True en producción con HTTPS
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# Mantener la sesión iniciada aunque se cierre el navegador
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # No expira al cerrar el navegador
SESSION_COOKIE_AGE = 1209600  # 2 semanas en segundos (ajustable)
SESSION_SAVE_EVERY_REQUEST = True  # Renueva la sesión en cada request

# Redirección después de cerrar sesión
LOGOUT_REDIRECT_URL = '/'

# Redirección para vistas protegidas por @login_required
LOGIN_URL = '/login/'

# Configuración de logs para depuración
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'WARNING',  # Cambia a 'ERROR' si quieres menos detalles
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'WARNING',  # Cambia a 'ERROR' para mostrar solo errores críticos
            'propagate': True,
        },
    },
}

# Configuración del backend de correo para pruebas
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')  # Tu correo de Gmail
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')  # La App Password de Google

DEFAULT_CONTACT_EMAIL = 'julian.lods@gmail.com'


# Dirección de correo predeterminada para contacto
DEFAULT_CONTACT_EMAIL = 'julian.lods@gmail.com'

# Configuración de MercadoPago
MERCADO_PAGO_ACCESS_TOKEN = "TEST-903676059026218-030618-7a178f9b228f0ec9e351e5edf13679bd-281041896"
MERCADO_PAGO_PUBLIC_KEY = "TEST-9cbf6f2e-602a-4b92-8ee3-bcf82321ad91"


# Storage backend de Cloudinary
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
