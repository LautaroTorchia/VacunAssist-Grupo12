# Generated by Django 4.0.4 on 2022-05-30 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Vacunation_app', '0002_alter_paciente_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='activo'),
        ),
    ]
