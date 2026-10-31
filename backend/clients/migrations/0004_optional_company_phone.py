# Regla vigente del desafío: empresa y teléfono vuelven a ser opcionales.

from django.core.validators import RegexValidator
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('clients', '0003_required_fields_and_name_validation')]
    operations = [
        migrations.AlterField(
            model_name='client', name='company',
            field=models.CharField(blank=True, max_length=150, verbose_name='empresa'),
        ),
        migrations.AlterField(
            model_name='client', name='phone',
            field=models.CharField(blank=True, max_length=30, verbose_name='teléfono', validators=[RegexValidator(
                regex=r'^\+?[0-9][0-9 ()-]{5,28}[0-9]$',
                message='Ingresa un teléfono de 7 a 30 caracteres con números, espacios, paréntesis o guiones. Puede comenzar con +.',
            )]),
        ),
    ]

