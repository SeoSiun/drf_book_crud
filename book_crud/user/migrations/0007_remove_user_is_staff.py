# Generated by Django 4.1.1 on 2022-09-14 04:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_user_is_staff'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_staff',
        ),
    ]