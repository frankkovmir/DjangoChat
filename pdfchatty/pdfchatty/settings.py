import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-9ymc$q(#lz283ub7+_+ghg)&65dh4lw+bs$n-5b72$ahfknh*^'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'chat',
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

ROOT_URLCONF = 'pdfchatty.urls'

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

WSGI_APPLICATION = 'pdfchatty.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CTRANSFORMERS = {
    'model_path': {
        'small': os.path.join(BASE_DIR, 'models', 'mistral-7b-instruct-v0.1.Q3_K_M.gguf'),
        'large': os.path.join(BASE_DIR, 'models', 'mistral-7b-instruct-v0.1.Q5_K_M.gguf'),
    },
    'model_type': 'mistral',
    'model_config': {
        'max_new_tokens': 256, #maximale Nummer der Antwort Token, je höher desto ggf. ausführlichere Antwort auf Kosten der Zeit
        'temperature': 0, # beeinflusst die "randomness" der Antwort bzw. wie deterministisch diese ist
        'context_length': 4096, # maximale Länge des Input Kontextes
        'gpu_layers': 0, #
        'threads': -1,
    },
}

CHAT_CONFIG = {
    'chat_memory_length': 2,
    'number_of_retrieved_documents': 3,
}

PDF_TEXT_SPLITTER = {
    'chunk_size': 1024, # Größe der "chunks" in characters in die das PDF zerlegt wird. Mehr heißt kleinere, größere Textabschnitte; das Modell muss es aber verarbeiten können
    'overlap': 100, # Sorgt dafür, dass Kontextinformationen zwischen chunks nicht verloren geht. Höhere Werte steigern Verständnis auf Kosten der Performance
    'separators': ["\n", "\n\n"],
}

EMBEDDINGS_PATH = os.path.join(BASE_DIR, 'models', 'e5-base-sts-en-de')

CHROMADB = {
    'chromadb_path': os.path.join(BASE_DIR, 'chroma_db'),
    'collection_name': 'pdfs',
}

CHAT_SESSIONS_DATABASE_PATH = os.path.join(BASE_DIR, 'chat_sessions', 'chat_sessions.db')

PDF_DIRECTORY = os.path.join(BASE_DIR, 'pdfs')
