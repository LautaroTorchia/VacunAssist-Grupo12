# Generated by Django 3.2.5 on 2022-05-11 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Vacunation_app', '0007_vacuna_vacunaenvacunatorio_vacunatorio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacuna',
            name='nombre',
            field=models.CharField(choices=[('GR', 'Gripe comun'), ('CAZ', 'COVID-Astrazeneca'), ('FA', 'Fiebre amarilla'), ('CPF', 'COVID-PFIEZER')], max_length=50),
        ),
    ]
