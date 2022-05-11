# Generated by Django 3.2.5 on 2022-05-11 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Vacunation_app', '0010_auto_20220511_1905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacuna',
            name='nombre',
            field=models.CharField(choices=[('CAZ', 'COVID-Astrazeneca'), ('FA', 'Fiebre amarilla'), ('CPF', 'COVID-PFIEZER'), ('GR', 'Gripe comun')], max_length=50),
        ),
    ]
