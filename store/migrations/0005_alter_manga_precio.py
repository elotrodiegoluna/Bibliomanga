# Generated by Django 4.2 on 2023-05-09 00:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_manga_precio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manga',
            name='precio',
            field=models.IntegerField(default=10000),
        ),
    ]
