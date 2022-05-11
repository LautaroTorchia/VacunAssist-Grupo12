# Generated by Django 3.2.5 on 2022-05-11 19:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Vacunation_app', '0009_auto_20220511_1902'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='dni',
            field=models.IntegerField(unique=True, validators=[django.core.validators.MaxValueValidator(15), django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='vacuna',
            name='nombre',
            field=models.CharField(choices=[('GR', 'Gripe comun'), ('CPF', 'COVID-PFIEZER'), ('FA', 'Fiebre amarilla'), ('CAZ', 'COVID-Astrazeneca')], max_length=50),
        ),
    ]
