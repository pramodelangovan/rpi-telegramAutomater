# Generated by Django 3.2.3 on 2021-05-16 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teleModel', '0003_rename_difference_goldrates_differencepergram'),
    ]

    operations = [
        migrations.AddField(
            model_name='goldrates',
            name='city',
            field=models.CharField(default='', max_length=256),
            preserve_default=False,
        ),
    ]
