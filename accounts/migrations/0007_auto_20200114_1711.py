# Generated by Django 2.2.5 on 2020-01-14 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20200114_1442'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='clusters',
            field=models.ManyToManyField(blank=True, to='decks.Cluster'),
        ),
    ]
