# Generated by Django 2.2.5 on 2020-01-21 10:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('decks', '0004_auto_20200120_1132'),
    ]

    operations = [
        migrations.RenameField(
            model_name='deck',
            old_name='position_north',
            new_name='position_latitude',
        ),
        migrations.RenameField(
            model_name='deck',
            old_name='position_east',
            new_name='position_longitude',
        ),
    ]
