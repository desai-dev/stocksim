# Generated by Django 4.1.4 on 2022-12-29 08:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cash',
            old_name='buyer',
            new_name='owner',
        ),
    ]
