# Generated by Django 4.1.1 on 2022-09-14 08:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_order_book_alter_order_create_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='create_at',
            new_name='created_at',
        ),
    ]
