from django.apps import AppConfig
from django.db import connection

class TothConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'toth'

    def ready(self):
        # Habilitar claves foráneas en SQLite
        with connection.cursor() as cursor:
            cursor.execute("PRAGMA foreign_keys = ON;")
