# Generated by Django 3.2.3 on 2021-05-19 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teleModel', '0005_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='isSuperAdmin',
            field=models.BooleanField(default=False),
        ),
    ]
