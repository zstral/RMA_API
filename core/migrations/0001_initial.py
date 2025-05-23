# Generated by Django 5.2 on 2025-05-02 01:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EstacionMeteorologica',
            fields=[
                ('codigo_nacional', models.IntegerField(primary_key=True, serialize=False)),
                ('codigo_omm', models.CharField(blank=True, max_length=10)),
                ('codigo_oaci', models.CharField(blank=True, max_length=10)),
                ('nombre', models.CharField(max_length=255)),
                ('latitud', models.FloatField()),
                ('longitud', models.FloatField()),
                ('altura', models.IntegerField()),
                ('region', models.IntegerField()),
                ('zona_geografica', models.CharField(max_length=100)),
                ('url_datos', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('rol', models.CharField(choices=[('user', 'User'), ('admin', 'Admin')], default='user', max_length=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
