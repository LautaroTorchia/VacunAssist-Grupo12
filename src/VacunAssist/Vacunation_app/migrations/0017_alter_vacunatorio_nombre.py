# Generated by Django 3.2.5 on 2022-05-11 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Vacunation_app', '0016_auto_20220511_1935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacunatorio',
            name='nombre',
            field=models.CharField(choices=[('Omnibus', 'Sede Omnibus'), ('Gonnet', 'Sede Gonnet'), ('Plaza Moreno', 'Sede Plaza Moreno')], max_length=50),
        ),
    ]
