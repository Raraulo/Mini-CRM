# Carga inicial de contactos ficticios; se aplica una sola vez.

"""Carga inicial, una sola vez. No crea cuentas de acceso ni contraseñas."""
import json
from importlib.resources import files

from django.db import migrations


def cargar_contactos(apps, schema_editor):
    Client = apps.get_model('clients', 'Client')
    datos = json.loads(files('base_de_datos').joinpath('contactos_prueba.json').read_text(encoding='utf-8'))
    database = schema_editor.connection.alias
    for contacto in datos:
        # No modifica registros existentes que tengan el mismo correo.
        if not Client.objects.using(database).filter(email=contacto['email']).exists():
            Client.objects.using(database).create(**contacto)


class Migration(migrations.Migration):
    dependencies = [('clients', '0001_initial')]
    operations = [migrations.RunPython(cargar_contactos, migrations.RunPython.noop)]

