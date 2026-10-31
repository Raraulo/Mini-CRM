# SQLite: ubicación del archivo persistente según el entorno de Docker.

"""Configuración de SQLite; Docker conserva el archivo en su volumen /data."""
import os
from pathlib import Path

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.environ.get('DJANGO_DB_PATH', Path(__file__).parent / 'db.sqlite3'),
    },
}
