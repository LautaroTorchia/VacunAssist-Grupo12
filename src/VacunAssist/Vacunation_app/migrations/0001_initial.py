# Generated by Django 4.0.4 on 2022-05-23 15:14

import Vacunation_app.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vacuna',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(choices=[('Gripe', 'Gripe Comun'), ('COVID-PFIZER', 'Covid F'), ('COVID-Astrazeneca', 'Covid Z'), ('Fiebre amarilla', 'Fiebre A')], max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vacunatorio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Zona',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(choices=[('Sede Omnibus', 'Omnibus'), ('Sede Cementerio', 'Cementerio'), ('Sede Municipalidad', 'Municipalidad')], max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('nombre_completo', models.CharField(max_length=50)),
                ('dni', models.CharField(max_length=15, unique=True, validators=[Vacunation_app.models.validate_decimal])),
                ('fecha_nac', models.DateTimeField()),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('clave', models.CharField(max_length=4)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VacunaEnVacunatorio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock', models.IntegerField(validators=[django.core.validators.MinValueValidator(1, 'Debe ingresar un numero mayor a 1')])),
                ('vacuna', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Vacunation_app.vacuna')),
                ('vacunatorio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Vacunation_app.vacunatorio')),
            ],
        ),
        migrations.CreateModel(
            name='Vacunador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tuvo_fiebre_amarilla', models.BooleanField()),
                ('dosis_covid', models.IntegerField(choices=[(1, 'Zero'), (2, 'One'), (3, 'Two')])),
                ('fecha_gripe', models.DateField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
