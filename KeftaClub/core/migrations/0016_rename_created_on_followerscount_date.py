# Generated by Django 5.0.6 on 2024-05-25 19:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_followerscount_created_on_alter_likepost_created_on'),
    ]

    operations = [
        migrations.RenameField(
            model_name='followerscount',
            old_name='created_on',
            new_name='date',
        ),
    ]
