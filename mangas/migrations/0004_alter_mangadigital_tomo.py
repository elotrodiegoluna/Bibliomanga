# Generated by Django 4.2.1 on 2023-06-10 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mangas', '0003_mangadigital_tomo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mangadigital',
            name='tomo',
            field=models.IntegerField(),
        ),
    ]
