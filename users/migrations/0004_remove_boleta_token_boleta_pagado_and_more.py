# Generated by Django 4.2.1 on 2023-06-01 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_boleta_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='boleta',
            name='token',
        ),
        migrations.AddField(
            model_name='boleta',
            name='pagado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='boleta',
            name='token_boleta',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]
