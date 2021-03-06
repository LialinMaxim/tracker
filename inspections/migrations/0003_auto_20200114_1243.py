# Generated by Django 2.2.5 on 2020-01-14 10:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import inspections.validators


class Migration(migrations.Migration):

    dependencies = [
        ('inspections', '0002_auto_20200113_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inspection',
            name='author',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='inspection_author', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='inspection',
            name='due_date',
            field=models.DateField(validators=[inspections.validators.validate_future_date]),
        ),
    ]
