# Generated by Django 4.0.4 on 2022-05-26 17:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Vacunation_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='zona',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='Vacunation_app.zona'),
        ),
    ]
