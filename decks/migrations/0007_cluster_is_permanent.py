# Generated by Django 2.2.5 on 2020-02-17 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('decks', '0006_auto_20200121_1241'),
    ]

    operations = [
        migrations.AddField(
            model_name='cluster',
            name='is_permanent',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
