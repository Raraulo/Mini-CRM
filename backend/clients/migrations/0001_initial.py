# Estructura inicial de la tabla de clientes.

from django.core.validators import RegexValidator
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='nombre')),
                ('company', models.CharField(blank=True, max_length=150, verbose_name='empresa')),
                ('email', models.EmailField(max_length=254, verbose_name='correo electrónico')),
                ('phone', models.CharField(blank=True, max_length=30, validators=[RegexValidator(
                    regex=r'^\+?[0-9][0-9 ()-]{5,28}[0-9]$',
                    message='Ingresa un teléfono de 7 a 30 caracteres con números, espacios, paréntesis o guiones. Puede comenzar con +.',
                )], verbose_name='teléfono')),
                ('status', models.CharField(choices=[('prospect', 'Prospecto'), ('customer', 'Cliente'), ('inactive', 'Inactivo')], default='prospect', max_length=10, verbose_name='estado')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='fecha de creación')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='última actualización')),
            ],
            options={
                'verbose_name': 'cliente', 'verbose_name_plural': 'clientes',
                'ordering': ['-created_at', '-pk'],
            },
        ),
    ]

