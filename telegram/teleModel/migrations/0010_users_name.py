# Generated by Django 3.2.3 on 2021-05-19 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teleModel', '0009_remove_users_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='name',
            field=models.CharField(default='', max_length=512),
        ),
    ]