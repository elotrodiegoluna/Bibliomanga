# Generated by Django 4.2.1 on 2023-05-14 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_alter_manga_precio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manga',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
