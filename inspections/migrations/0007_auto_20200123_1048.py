# Generated by Django 2.2.5 on 2020-01-23 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inspections', '0006_auto_20200121_1216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inspection',
            name='completed_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
