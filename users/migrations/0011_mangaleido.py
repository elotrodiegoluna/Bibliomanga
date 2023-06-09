# Generated by Django 4.2.1 on 2023-06-10 02:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mangas', '0002_mangadigital_timestamp'),
        ('users', '0010_user_date_joined'),
    ]

    operations = [
        migrations.CreateModel(
            name='MangaLeido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_page', models.IntegerField(null=True)),
                ('finished', models.BooleanField(default=False)),
                ('manga', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mangas.mangadigital')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
