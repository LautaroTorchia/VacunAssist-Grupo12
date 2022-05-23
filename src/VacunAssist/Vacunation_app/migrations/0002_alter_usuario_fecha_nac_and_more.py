# Generated by Django 4.0.4 on 2022-05-23 02:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Vacunation_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='fecha_nac',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='vacunaenvacunatorio',
            name='stock',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1, 'Debe ingresar un numero mayor a 1')]),
        ),
    ]