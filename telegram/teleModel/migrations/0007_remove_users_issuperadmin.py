# Generated by Django 3.2.3 on 2021-05-19 09:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teleModel', '0006_users_issuperadmin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='isSuperAdmin',
        ),
    ]