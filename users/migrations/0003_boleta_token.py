# Generated by Django 4.2.1 on 2023-06-01 04:40

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_boleta'),
    ]

    operations = [
        migrations.AddField(
            model_name='boleta',
            name='token',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
