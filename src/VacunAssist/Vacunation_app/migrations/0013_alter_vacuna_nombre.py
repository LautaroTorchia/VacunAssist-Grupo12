# Generated by Django 3.2.5 on 2022-05-11 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Vacunation_app', '0012_auto_20220511_1908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacuna',
            name='nombre',
            field=models.CharField(choices=[('Covid-F', 'COVID-PFIEZER'), ('fiebreA', 'Fiebre amarilla'), ('Covid-Z', 'COVID-Astrazeneca'), ('Gripe', 'Gripe comun')], max_length=50),
        ),
    ]