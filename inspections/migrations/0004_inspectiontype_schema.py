# Generated by Django 2.2.5 on 2020-01-16 16:14

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('inspections', '0003_auto_20200114_1243'),
    ]

    operations = [
        migrations.AddField(
            model_name='inspectiontype',
            name='schema',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default='{}'),
        ),
    ]
