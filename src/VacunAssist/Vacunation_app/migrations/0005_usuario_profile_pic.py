# Generated by Django 4.0.4 on 2022-06-02 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Vacunation_app', '0004_remove_usuario_avatar_turno'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='profile_pic',
            field=models.ImageField(default='profile_pic.png', upload_to=''),
        ),
    ]
