# Generated by Django 4.2.11 on 2024-05-05 11:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_post_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='birthDate',
            field=models.DateTimeField(default=datetime.datetime(2000, 1, 1, 0, 0)),
        ),
    ]
