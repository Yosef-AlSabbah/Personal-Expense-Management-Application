# Generated by Django 5.1.3 on 2024-11-12 17:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicaluseraccount',
            name='is_verified',
        ),
        migrations.RemoveField(
            model_name='useraccount',
            name='is_verified',
        ),
    ]